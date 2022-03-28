use proconio::input;
use array_macro::*;

pub fn slove() {
    // Step #1. 入力
    input! {
        n: i32,
        l: i32,
        k: i32,
    }
    const LEN:usize = 1000000000;
    let a: [i32; LEN] = array![1; LEN];

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
    println!("{}", left);
}