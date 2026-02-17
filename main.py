from orbit.propogate import satellite_positions

def main():
    sats = satellite_positions()
    for i in sats[:5]:
        print(i["name"], i["position_km"])

if __name__ == "__main__":
    main()

