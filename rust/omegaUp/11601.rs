use std::io::{self, BufRead, Write};

fn main() {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut out = io::BufWriter::new(stdout.lock());

    let mut lines = stdin.lock().lines();

    let first_line = lines.next().unwrap().unwrap();
    let mut iter = first_line.split_whitespace();
    let n: usize = iter.next().unwrap().parse().unwrap();
    let m: usize = iter.next().unwrap().parse().unwrap();

    let mut v = vec![0usize; m + 1];

    let second_line = lines.next().unwrap().unwrap();
    for token in second_line.split_whitespace() {
        let o: usize = token.parse().unwrap();
        if o > 0 && o <= m {
            v[o] += 1;
        }
    }

    for i in 1..=m {
        writeln!(out, "{}: {}", i, v[i]).unwrap();
    }
}