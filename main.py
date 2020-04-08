import os
import mel_parser


def main():
    prog = '''
        int[] b = { a, b , {c, d } };
        int[] b = new int[b + c][4];
        int[] b = 4;
        int g, g2 = g, g = 90;

        a = input(); b = input();  /* comment 1
        c = input();
        */

        //int [ ] b = int [ 5 ];
        //a = int[5];
        string b = "Привет";
        //a . g2;
        for (int i = 0, j = 8; ((i <= 5)) && g; i = i + 1, print(5))
            for(; a < b;)
                if (a > 7 + b) {
                    c = a+b * (2 - 1) + 0;  // comment 2
                    b = "98\tура";
                }
                else if (f)            
                    output(c + 1, 89.89);
        for(;;);
        while (g2 > g)
            output(g2);
    '''
    prog = mel_parser.parse(prog)
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
