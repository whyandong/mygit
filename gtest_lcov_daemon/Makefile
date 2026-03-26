CC = gcc
CXX = g++
CFLAGS = -g -O0 -fprofile-arcs -ftest-coverage -Iinclude
CXXFLAGS = -g -O0 -fprofile-arcs -ftest-coverage -Iinclude
LDFLAGS = -fprofile-arcs -ftest-coverage
GTEST_LIBS = -lgtest -lgtest_main -lpthread

SRCS = src/daemon.c
OBJS = $(SRCS:.c=.o)
TEST_SRCS = test/test_daemon.cpp
TEST_OBJS = $(TEST_SRCS:.cpp=.o)

.PHONY: all test run coverage clean

all: test

src/daemon.o: src/daemon.c
    $(CC) $(CFLAGS) -DUNIT_TEST -c $< -o $@

%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@

%.o: %.cpp
    $(CXX) $(CXXFLAGS) -c $< -o $@

test: $(OBJS) $(TEST_OBJS)
    $(CXX) $(LDFLAGS) -o run_tests $(OBJS) $(TEST_OBJS) $(GTEST_LIBS)

run: test
    # reset counters (optional)
    lcov --directory . --zerocounters
    ./run_tests

coverage: run
    # capture coverage data
    lcov --directory . --capture --output-file coverage.info
    # remove system and test files from report
    lcov --remove coverage.info '/usr/*' '*/test/*' -o coverage.filtered.info
    genhtml coverage.filtered.info --output-directory coverage-report
    @echo "Open coverage-report/index.html"

clean:
    rm -f src/*.o test/*.o *.o run_tests *.gcda *.gcno coverage*.info
    rm -rf coverage-report
