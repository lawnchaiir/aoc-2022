use std::{collections::HashSet, fs::File, io::Read, path::Path};

fn main() {
    let input = load_input();

    let lines = input.split_ascii_whitespace().map(|s| String::from(s));

    let mut first_range_set: HashSet<u32> = HashSet::new();
    let mut second_range_set: HashSet<u32> = HashSet::new();

    let mut fully_contained_count: u32 = 0;
    let mut overlap_count: u32 = 0;

    for line in lines {
        let mut pair = line.split_terminator(",");

        let first_range = create_range_from_string(pair.next().unwrap());
        let second_range = create_range_from_string(pair.next().unwrap());

        first_range_set.clear();
        second_range_set.clear();

        first_range_set.extend(first_range);
        second_range_set.extend(second_range);

        if first_range_set.is_superset(&second_range_set)
            || first_range_set.is_subset(&second_range_set)
        {
            fully_contained_count += 1;
        }

        if first_range_set
            .intersection(&second_range_set)
            .next()
            .is_some()
        {
            overlap_count += 1;
        }
    }

    println!("Fully contained={}", fully_contained_count);
    println!("Overlaps={}", overlap_count);
}

fn create_range_from_string(s: &str) -> std::ops::RangeInclusive<u32> {
    let mut range_spec = s.split_terminator("-");
    let range_start = range_spec.next().unwrap().parse::<u32>().unwrap();
    let range_end = range_spec.next().unwrap().parse::<u32>().unwrap();

    return range_start..=range_end;
}

fn load_input() -> String {
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
