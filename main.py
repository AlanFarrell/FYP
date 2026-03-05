from orbit.VisibilityWindow import coverage_time
from orbit.gantt import gantt

def main():
    coverage = coverage_time()

    print("Coverage windows:")
    for ws, we in coverage["windows"]:
        print(f" - ({ws.strftime('%H:%M:%S')}, {we.strftime('%H:%M:%S')})")

    print("Total coverage(mins):", coverage["total(mins)"])
    print("Average window of coverage(mins):", coverage["avg_coverage(mins)"])
    print("Coverage time %:", coverage["coverage_percent"])

    gantt(coverage["windows"])

if __name__ == "__main__":
    main()

