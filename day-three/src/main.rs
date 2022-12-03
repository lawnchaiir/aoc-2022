use std::{path::Path, fs::File, io::Read, collections::HashSet};

fn main() {
    let s = load();

    let lines : Vec<String> = s.split_ascii_whitespace().map(|s| String::from(s)).collect();

    let mut total_score : u32 = 0;
    for l in &lines {
        let length = l.len();
        let compartment_size = length / 2;
        let (first_compartment, second_compartment) = l.split_at(compartment_size);

        let first_unique: HashSet<char> = first_compartment.chars().collect();
        let sec_unique: HashSet<char> = second_compartment.chars().collect();

        let overlap = first_unique.intersection(&sec_unique);

        for c in overlap {
            total_score += score_char(*c);
        }
    }

    println!("{}", total_score );


    total_score = 0;

    for i in (0..lines.len()).step_by(3) {
        // There's got to be a better way to do this ... this will do for now
        let first_elf : &HashSet<char> = &lines[i].chars().collect();
        let sec_elf : &HashSet<char> = &lines[i + 1].chars().collect();
        let third_elf : &HashSet<char> = &lines[i + 2].chars().collect();

        let intersect: &HashSet<char> = &(first_elf & sec_elf);
        
        let badge = intersect & third_elf;
        // not robust, relying on the assumption that's given in the problem, that there will always be one match
        total_score += score_char(*badge.iter().next().unwrap());
    }

    println!("{}", total_score);

}

fn score_char(c:char) -> u32 {
    let mut score = (c as u32) & 31; // bit trick to reduce char to its alphabetical position
    if c.is_uppercase() {
        score += 26;
    }
    return score;
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
    return s;
}