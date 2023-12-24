import itertools
import sympy

START = 200000000000000
END = 400000000000000


def get_puzzle_input():
    with open("input.txt", "r") as file:
        lines = [line.strip().split(" @ ") for line in file.readlines()]
        return [(tuple(int(i) for i in pos.split(", ")), tuple(int(i) for i in vel.split(","))) for pos, vel in lines]


def intersects(a, b):
    # aus den startpunkten und steigungen der beiden stürme werden formel gemacht, welche für jede x position die
    # passende y position als ergebnis haben (lineare formel der form f(x) = mx + b).
    # dafür muss um die steigung von x skaliert und um den startpunkt von x verschoben werden.
    # skalieren der steigung einer linearen formel um faktor s: f(x) = (s * m) * x + b
    # verschieben einer linearen formel um faktor s: f(x) = m * (x - s) + b
    (apx, apy, _), (avx, avy, _) = a
    (bpx, bpy, _), (bvx, bvy, _) = b

    # skaliere steigung von y um steigung von x
    am = avy / avx
    bm = bvy / bvx

    if am == bm:
        # steigungen sind parallel und können deswegen nicht schneiden
        return False

    # neue lineare formeln aufstellen (beispiel für sturm a):
    # f(x) = (avy / avx) * (x - apx) + apy
    # die steigung ist skaliert um faktor avx und verschoben um startpunkt apx

    # gleichsetzen der beiden neuen formel für a und b
    # am * (x - apx) + apy = bm * (x - bpx) + bpy
    # am * x - am * apx + apy = bm * x - bm * bpx + bpy
    # (am - bm) * x = am * apx - apy - bm * bpx + bpy
    # x = (am * apx - apy - bm * bpx + bpy) / (am - bm)
    x = (am * apx - apy - bm * bpx + bpy) / (am - bm)

    # einsetzen in eine der formeln, um y zu ermitteln
    y = (am * (x - apx)) + apy

    # zeitpunkt ermitteln, an dem punkt x erreicht wurde.
    # wenn dieser bei einer der beiden formel in der vergangenheit liegt, zählt die überschneidung nicht
    if (x - apx) / avx < 0 or (x - bpx) / bvx < 0:
        return False

    # kontrolliere, ob überschneidung in unserem testbereich liegt
    return START <= x <= END and START <= y <= END


def first_puzzle():
    lines = get_puzzle_input()
    result = sum(intersects(a, b) for a, b in itertools.combinations(lines, 2))
    print(f"Puzzle 1: {result}")


def second_puzzle():
    # dafür hab ich nicht genug mathe im studium gehabt.
    # --> stelle ein algebraischen gleichungssystem auf und lasse das von einem solver lösen <--
    hailstones = get_puzzle_input()

    # symbole für den stein anlegen (start x, start y, start z, velocity x, velocity y, velocity z)
    rpx, rpy, rpz, rvx, rvy, rvz = [sympy.Symbol(symbol_name) for symbol_name in "rpx,rpy,rpz,rvx,rvy,rvz".split(",")]

    equations = []
    time_symbols = []
    for i, ((hpx, hpy, hpz), (hvx, hvy, hvz)) in enumerate(hailstones[:3]):
        # stelle das gleichungssystem für 3 stürme auf.
        # theoretisch ist es möglich, dass wir hier eine schlechte auswahl treffen und es mehrere lösungen für diese
        # 3 stürme gibt. ein testlauf zeigt aber, das für die ersten 3 stürme nur eine lösung existiert. mehr muss hier
        # also nicht abgefragt werden.

        # erstelle ein symbol für den zeitpunkt, an dem der stein den sturm trifft
        time = sympy.Symbol(f"t_{i}")
        time_symbols.append(time)

        # gleichsetzen aller 3 dimensionen nach t schritten mit dem stein
        # (stein_velocity * time + stein_start) == (sturm_velocity * time + sturm_start)
        # sympy erwartet hier gleichungen die gleich 0 gesetzt sind, also vorher umstellen
        equations.append((rvx * time + rpx) - (hvx * time + hpx))
        equations.append((rvy * time + rpy) - (hvy * time + hpy))
        equations.append((rvz * time + rpz) - (hvz * time + hpz))

    # magic
    symbol_values = sympy.solve_poly_system(equations, [rpx, rpy, rpz, rvx, rvy, rvz, *time_symbols])[0]

    # start x + start y + start z
    result = symbol_values[0] + symbol_values[1] + symbol_values[2]
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 14672
    second_puzzle()  # Puzzle 2: 646810057104753
