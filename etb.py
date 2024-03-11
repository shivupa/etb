from pyscf import gto
import sys

l = {"s": 0, "p": 1, "d": 2, "f": 3, "g": 4, "h": 5, "i": 6}
ang_mom_to_string = ["s", "p", "d", "f", "g", "h", "i"]

import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i","--input",
        type=str,
        default="input.txt",
        help="input file. First line atom, second line-nth line : l, n, alpha, beta.",
    )
    parser.add_argument(
        "-exi","--exinput", type=str, default=argparse.SUPPRESS, help="example input file"
    )
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    return args


def example_input(filename):
    with open(filename, "w") as f:
        f.write("X # atom name\n")
        for l_lab, l_val in l.items():
            n = 1
            alpha = 1.0
            beta = 1.0/3.0
            f.write(
                f"{l_lab}    {n: 4d}    {alpha:12.8f}    {beta:12.8f} # angular momentum, num func, initial alpha, ration between alpha+1/alpha\n"
            )


def create_basis(filename):
    basis_shells = []
    with open(filename, "r") as f:
        atom = None
        for line in f:
            if atom is None:
                atom = line.strip()
            else:
                l_lab, n, alpha, beta = line.split()
                basis_shells.append((l[l_lab], int(n), float(alpha), float(beta)))

    basis = gto.expand_etbs(basis_shells)

    print(f"****\n{atom}     0")
    for l_val, func in basis:
        print(f"{ang_mom_to_string[l_val]}  1   1.0\n    {func[0]: 14.10f}    {func[1]}")
    print("****")


if __name__ == "__main__":
    args = get_args()
    print(args)

    if "exinput" in args:
        example_input(args.exinput)
    else:
        create_basis(args.input)
