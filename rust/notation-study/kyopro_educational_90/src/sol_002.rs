use proconio::input;

fn hantei(s: &String) -> bool {
    let mut dep = 0;
    let chars = s.chars().collect::<Vec<char>>();
    for i in 0..chars.len() {
        if chars[i] == '(' {
            dep += 1;
        }
        if chars[i] == ')' {
            dep -= 1;
        }
        if dep < 0 {
            return false;
        }
    }
    dep == 0
}

fn solve(n: i32) -> Vec<String>{
    let mut answer: Vec<String> = Vec::new();
    for i in 0..(1 << n) {
        let mut candidate: String = String::new();
        let mut j = n - 1;
        while j >= 0 {
            if (i & (1 << j)) == 0 {
                candidate += "(";
            }
            else {
                candidate += ")";
            }
            j = j - 1;
        }
        if hantei(&candidate) {
            println!("{}", candidate);
            answer.push(candidate);
        }
    }
    answer
}

pub fn call_solve() {
    // Step #1. 入力
    println!("Nは？");
    input! {
        n: i32,
    }
    solve(n);
}

#[cfg(test)]
mod tests
{
    use super::solve;
    #[test]
    fn test1() {
        let answer = vec!["()".to_string()];
        let ret = solve(2);
        assert_eq!(ret, answer);
    }
    #[test]
    fn test2() {
        let answer: Vec<String> = vec![];
        let ret = solve(3);
        assert_eq!(ret, answer);
    }
    #[test]
    fn test3() {
        let answer = vec!["(())".to_string(), "()()".to_string()];
        let ret = solve(4);
        assert_eq!(ret, answer);
    }
    #[test]
    fn test4() {
        let answer = vec![
            "((((()))))".to_string(),
            "(((()())))".to_string(),
            "(((())()))".to_string(),
            "(((()))())".to_string(),
            "(((())))()".to_string(),
            "((()(())))".to_string(),
            "((()()()))".to_string(),
            "((()())())".to_string(),
            "((()()))()".to_string(),
            "((())(()))".to_string(),
            "((())()())".to_string(),
            "((())())()".to_string(),
            "((()))(())".to_string(),
            "((()))()()".to_string(),
            "(()((())))".to_string(),
            "(()(()()))".to_string(),
            "(()(())())".to_string(),
            "(()(()))()".to_string(),
            "(()()(()))".to_string(),
            "(()()()())".to_string(),
            "(()()())()".to_string(),
            "(()())(())".to_string(),
            "(()())()()".to_string(),
            "(())((()))".to_string(),
            "(())(()())".to_string(),
            "(())(())()".to_string(),
            "(())()(())".to_string(),
            "(())()()()".to_string(),
            "()(((())))".to_string(),
            "()((()()))".to_string(),
            "()((())())".to_string(),
            "()((()))()".to_string(),
            "()(()(()))".to_string(),
            "()(()()())".to_string(),
            "()(()())()".to_string(),
            "()(())(())".to_string(),
            "()(())()()".to_string(),
            "()()((()))".to_string(),
            "()()(()())".to_string(),
            "()()(())()".to_string(),
            "()()()(())".to_string(),
            "()()()()()".to_string(),
            ];
        let ret = solve(10);
        assert_eq!(ret, answer);
    }
}