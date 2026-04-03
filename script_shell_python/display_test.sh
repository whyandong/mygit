#!/usr/bin/env bash
# multi_ppi.sh - 自动获取所有屏幕的分辨率和物理尺寸，计算 PPI

set -euo pipefail
# --------------------------
# 功能1：计算屏幕 PPI
# --------------------------
calc_ppi() {
  XRANDR_INFO=$(xrandr -d :0 --query | grep " connected" | grep -E '^.+[0-9]+x[0-9]+\+[0-9]+\+[0-9]+')

  if [[ -z "$XRANDR_INFO" ]]; then
    echo "未检测到任何屏幕"
    exit 1
  fi

  echo "---- 屏幕 PPI 信息 ----"

  # 遍历每个已连接屏幕
  echo "$XRANDR_INFO" | while read -r line; do
    NAME=$(echo "$line" | awk '{print $1}')
    RESOLUTION=$(echo "$line" | grep -oP '\d+x\d+\+' | head -n1 | tr -d '+')
    WIDTH_PX=$(echo "$RESOLUTION" | cut -d'x' -f1)
    HEIGHT_PX=$(echo "$RESOLUTION" | cut -d'x' -f2)

    PHYS_W_MM=$(echo "$line" | grep -oP '\d+mm x \d+mm' | awk '{print $1}' | tr -d 'mm')
    PHYS_H_MM=$(echo "$line" | grep -oP '\d+mm x \d+mm' | awk '{print $3}' | tr -d 'mm')

    # 有些显示器可能不会报告物理尺寸
    if [[ -z "$PHYS_W_MM" || -z "$PHYS_H_MM" ]]; then
      echo "显示器 $NAME: 分辨率 ${WIDTH_PX}x${HEIGHT_PX}, 未能获取物理尺寸，无法计算 PPI"
      continue
    fi

    PHYS_W_IN=$(awk -v w="$PHYS_W_MM" 'BEGIN {printf "%.6f", w * 0.0393701}')
    PHYS_H_IN=$(awk -v h="$PHYS_H_MM" 'BEGIN {printf "%.6f", h * 0.0393701}')

    PIX_DIAG=$(awk -v w="$WIDTH_PX" -v h="$HEIGHT_PX" 'BEGIN {printf "%.6f", sqrt(w*w + h*h)}')
    PHYS_DIAG=$(awk -v w="$PHYS_W_IN" -v h="$PHYS_H_IN" 'BEGIN {printf "%.6f", sqrt(w*w + h*h)}')

    PPI=$(awk -v pd="$PIX_DIAG" -v di="$PHYS_DIAG" 'BEGIN {if(di>0) printf "%.2f", pd / di; else print "NaN"}')

    echo "显示器: $NAME"
    echo "  分辨率: ${WIDTH_PX} x ${HEIGHT_PX} px"
    echo "  物理尺寸: ${PHYS_W_MM} mm x ${PHYS_H_MM} mm"
    echo "  像素对角线: ${PIX_DIAG} px"
    echo "  物理对角线: ${PHYS_DIAG} in"
    echo "  像素密度 (PPI): ${PPI} ppi"
    echo "-----------------------"
  done
}

# --------------------------
# 功能2：获取所有的缩放值，测试过程中确保缩放值一致
# --------------------------
get_display_scale() {
	if [ `ps  -elf | grep plasmashell | wc -l` -le 1 ];then
            echo 	"未正常进入桌面"
	else
  			echo "xrandr中屏幕配置值"
                        xrandr -d :0
  			echo "环境变量中缩放值"
  			pid=`ps -elf | grep '/usr/bin/plasmashell' | grep -v grep | awk '{print $4}'`
  			cat /proc/$pid/environ | tr '\0' '\n'  | grep QT
  			#export | grep QT 
  			echo "配置文件中缩放值"
  			cat /home/$USER/.config/kdeglobals | grep -A 5 KScreen
  			echo "设置中缩放值"
  			busctl --user get-property com.nfs.daemon.Display /com/nfs/daemon/Display com.nfs.daemon.Display scaleFactor 
  			echo   ".locale中kscreen的配置文件信息"
  			for i in `ls /home/$USER/.local/share/kscreen/control/configs/`;do
                  			echo $i
                			cat  /home/$USER/.local/share/kscreen/control/configs/$i
  			done
 	fi
}

# --------------------------
# 功能3：删除显示配置
# --------------------------
clear_display_config() {
  echo "⚠️ 将清空 KDE 显示配置并请求注销..."
  rm -rf /home/$USER/.local/share/kscreen/* 2>/dev/null || true
  sed -i '/^\[KScreen\]$/, /^\[WM\]$/{//!d}' /home/$USER/.config/kdeglobals 2>/dev/null || true
  echo "✅ 已删除显示配置并请求注销"
  busctl --user call com.nfs.SessionManager /com/nfs/SessionManager com.nfs.SessionManager RequestLogout "i" 0 || true
}

# --------------------------
# 功能4：注销
# --------------------------
menu_logout() {
  echo "⚠️ 将注销当前用户..."
  busctl --user call com.nfs.SessionManager /com/nfs/SessionManager com.nfs.SessionManager RequestLogout "i" 0 || true
}

# --------------------------
# 菜单交互
# --------------------------
while true; do
  echo
  echo "==============================="
  echo "   🖥️  显示需求辅助测试工具"
  echo "==============================="
  echo "1️  计算屏幕 PPI "
  echo "2️  查看所有缩放值"
  echo "3️  清除 KDE 显示配置并注销"
  echo "4  注销"
  echo "5  退出"
  echo "==============================="
  read -rp "请选择操作 [1-4]: " choice
  echo

  case "$choice" in
    1) calc_ppi ;;
    2) get_display_scale ;;
    3) clear_display_config ;;
    4) menu_logout ;;
    5) echo "退出程序"; exit 0 ;;
    *) echo "无效选项，请输入 1-4";;
  esac
done
