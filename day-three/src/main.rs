use std::{collections::HashSet, fs::File, io::Read, path::Path};

fn main() {
    let s = load();

    let lines: Vec<String> = s
        .split_ascii_whitespace()
        .map(|s| String::from(s))
        .collect();

    let mut total_score: u32 = 0;
    for l in &lines {
        let compartment_size = l.len() / 2;
        let (first_compartment, second_compartment) = l.split_at(compartment_size);

        let first_unique: HashSet<char> = first_compartment.chars().collect();
        let sec_unique: HashSet<char> = second_compartment.chars().collect();

        let overlap = first_unique.intersection(&sec_unique);

        for c in overlap {
            total_score += score_char(*c);
        }
    }

    println!("{}", total_score);

    total_score = 0;

    let mut first_elf: HashSet<char> = HashSet::new();
    let mut second_elf: HashSet<char> = HashSet::new();
    let mut third_elf: HashSet<char> = HashSet::new();

    let mut intersection: HashSet<char> = HashSet::new();
    for i in (0..lines.len()).step_by(3) {
        first_elf.clear();
        second_elf.clear();
        third_elf.clear();

        first_elf.extend(lines[i].chars());
        second_elf.extend(lines[i + 1].chars());
        third_elf.extend(lines[i + 2].chars());

        let first_intersection = first_elf.intersection(&second_elf);

        intersection.clear();
        intersection.extend(first_intersection);

        let mut badge = intersection.intersection(&third_elf);
        // not robust, relying on the assumption that's given in the problem, that there will always be one match
        total_score += score_char(*badge.next().unwrap());
    }

    println!("{}", total_score);
}

fn score_char(c: char) -> u32 {
    let mut score = (c as u32) & 31; // bit trick to reduce char to its alphabetical position
    if c.is_uppercase() {
        score += 26;
    }

    return score;
}

fn load() -> String {
    let path = Path::new("input.txt");
    let display = path.display();

    let mut file = match File::open(&path) {
        Err(why) => panic!("couldn't open {}: {}", display, why),
        Ok(file) => file,
    };

    let mut s: String = String::new();
    file.read_to_string(&mut s).expect("couldn't read");
    return s;
}
