use std::env;
mod sol_001;
mod sol_002;

fn main() {
    let args: Vec<String> = env::args().collect();
    let problem_id = args[1].parse::<i32>().unwrap();
    match problem_id {
        1 => sol_001::call_solve(),
        2 => sol_002::call_solve(),
        //3 => sol_003::call_solve(),
        _ => println!("The sol {} couldn't find.", problem_id)
    }
}
