from orbit.VisibilityWindow import coverage_time
from orbit.gantt import gantt
from CoverageMaps.CoverageTime import coverage_map



#Checking satellite coverage from 2026-03-14 23:57:51.463535+00:00 to 2026-03-15 23:57:51.463535+00:00

def main():
    coverage_map()

    # coverage = coverage_time(51.898150, -8.473796)
    #
    # print("Coverage windows:")
    # for ws, we in coverage["windows"]:
    #     print(f" - ({ws.strftime('%H:%M:%S')}, {we.strftime('%H:%M:%S')})")
    #
    # print("Total coverage(mins):", coverage["total(mins)"])
    # print("Average window of coverage(mins):", coverage["avg_coverage(mins)"])
    # print("Coverage time %:", coverage["coverage_percent"])
    #
    # gantt(coverage["windows"])

if __name__ == "__main__":
    main()

