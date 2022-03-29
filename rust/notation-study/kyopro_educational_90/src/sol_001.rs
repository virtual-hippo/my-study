use proconio::input;
use std::io;

pub fn solve() {
    // Step #1. 入力
    println!("N, L, Kの順で入力してください");
    input! {
        n: i32,
        l: i32,
        k: i32,
    }
    const LEN: usize = 1000000000;
    // declear as Vec in order to avoid stack overflow
    //let mut a: [i32; LEN] = [0; LEN];
    let mut a = vec![0; LEN];

    for i in 1..=n {
        println!("A[{}]を入力してください", i);
        let mut number = String::new();
        io::stdin().read_line(&mut number).ok();
        a[i as usize] = number.trim().parse().ok().unwrap();
    }

    let is_ok = |mid| {
        let (mut cnt, mut pre) = (0, 0);
        for i in 1..=n {
            if a[i as usize] - pre >= mid && l - a[i as usize] >= mid {
                cnt += 1;
                pre = a[i as usize];
            }
        }
        if cnt >= k {
            true
        } else {
            false
        }
    };
    
    // Step #2. 答えで二分探索（めぐる式二分探索法）
    // https://qiita.com/drken/items/97e37dd6143e33a64c8c
    let mut left = -1;
    let mut right = l + 1;
    while right - left > 1 {
        let mid = left + (right - left) / 2;
        if is_ok(mid) == false {
            right = mid
        } else {
            left = mid;
        }
    }
    println!("Answer: {}", left);
}
