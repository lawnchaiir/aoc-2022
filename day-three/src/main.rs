use std::{path::Path, fs::File, io::Read, collections::HashSet};

fn main() {
    let s = load();

    let lines = s.split_ascii_whitespace();

    let mut total_score : u32 = 0;
    for l in lines {
        let length = l.len();
        let compartment_size = length / 2;
        let (first_compartment, second_compartment) = l.split_at(compartment_size);

        let first_unique: HashSet<char> = first_compartment.chars().collect();
        let sec_unique: HashSet<char> = second_compartment.chars().collect();

        let overlap = first_unique.intersection(&sec_unique);

        for c in overlap {
            
            let mut score = (*c as u32) & 31;
            if c.is_uppercase() {
                score += 26;
            }
            total_score += score;
            println!("{}, {}",c , score)
        }
    }

    println!("{}", total_score );
}

fn load() -> String {
    let path = Path::new("input.txt");
    let display = path.display();

    let mut file  = match File::open(&path) {
        Err(why) => panic!("couldn't open {}: {}", display, why),
        Ok(file) => file,
    };

    let mut s : String = String::new();
    file.read_to_string(&mut s).expect("couldn't read");
    return  s;
}