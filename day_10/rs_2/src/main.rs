use std::io::BufReader;
use std::fs::File;
use std::io::prelude::*;
use std::collections::HashSet;
use std::collections::HashMap;

#[derive(Debug, Eq, PartialEq, Copy, Clone)]
struct Asteroid {
    x : usize,
    y : usize,
}

trait Detector {
    fn detect_asteroids(&self, asteroids: &Vec<Asteroid>) -> usize;
}

trait Vaporizer {
    fn vaporize_asteroids(&self, asteroids: &Vec<Asteroid>) -> Option<Vec<Asteroid>>;
}

fn gcd(x: i64, y: i64) -> i64 {
    if x < 0 {
        gcd(x.abs(), y)
    }
    else if y < 0 {
        gcd(x, y.abs())
    }
    else if y == 0 {
        x
    }
    else {
        gcd(y, x % y)
    }
}

impl Detector for Asteroid {
    fn detect_asteroids(&self, asteroids: &Vec<Asteroid>) -> usize {
        let asteroids_except_self: Vec<&Asteroid> = 
            asteroids.iter().filter(|a| *a != self).collect();        
        
        let mut unique_slopes: HashSet<(i64, i64)> = HashSet::new();
        for asteroid in asteroids_except_self {
            let dx = (asteroid.x as i64) - (self.x as i64);
            let dy = (asteroid.y as i64) - (self.y as i64);
            let x = dx / gcd(dx, dy);
            let y = dy / gcd(dx, dy);
            let current = (x, y);
            unique_slopes.insert(current);
        }
        unique_slopes.len()
    }
}

fn compute_atan2(a: &Asteroid, b: &Asteroid) -> f64 {
    let x = (a.x as i64 - b.x as i64) as f64;
    let y = (a.y as i64 - b.y as i64) as f64;
    return -x.atan2(y);
}

fn order_by_atan2(a: &Asteroid, b: &Asteroid, c: &Asteroid) -> std::cmp::Ordering {
    let first = compute_atan2(a, c);
    let second = compute_atan2(b, c);
    if first == second {
        return std::cmp::Ordering::Equal
    }
    else if first > second {
        return std::cmp::Ordering::Greater
    }

    std::cmp::Ordering::Less
}

impl Vaporizer for Asteroid {
    fn vaporize_asteroids(&self, asteroids: &Vec<Asteroid>) -> Option<Vec<Asteroid>> {
        if asteroids.len() == 0 {
            return None;
        }

        let mut vaporized: Vec<Asteroid> = Vec::new();
        vaporized.push(self.clone());
        while vaporized.len() < asteroids.len() {
            let mut closest_points = HashMap::new();
            for asteroid in asteroids {
                if !vaporized.contains(&asteroid) {
                    let dx = (asteroid.x as i64) - (self.x as i64);
                    let dy = (asteroid.y as i64) - (self.y as i64);
                    let x = dx / gcd(dx, dy);
                    let y = dy / gcd(dx, dy);
                    let key = (x, y);
                    if !closest_points.contains_key(&key) {
                        closest_points.insert(key, asteroid.clone());
                    }
                    else {
                        let closest = closest_points.get(&key).unwrap();
                        let current_value = (asteroid.x as i64 - self.x as i64).abs() + (asteroid.y as i64 - self.y as i64).abs();
                        let closest_value = (closest.x as i64 - self.x as i64).abs() + (closest.y as i64 - self.y as i64);
                        if  current_value < closest_value {
                            closest_points.insert(key, asteroid.clone());
                        }
                    }
                }
            }
            let mut buffer = Vec::new();
            closest_points.values().for_each(|v| buffer.push(v.clone()));
            buffer.sort_by(|a, b| order_by_atan2(a, b, self));
            buffer.iter().for_each(|a| vaporized.push(a.clone()));
        }
        Some(vaporized)
    }
}

fn read_aseroid_data(path:&str) -> std::io::Result<Vec<Asteroid>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut buffer = Vec::new();
    for (y, line_result) in reader.lines().enumerate() {
        let line = line_result.unwrap();
        for (x, c) in line.chars().enumerate() {
            match c {
                '#' => buffer.push(Asteroid {x: x, y: y}),
                '.' => (),
                _ => panic!("Unexpected character in file."),
            }
        }
    }
    Ok(buffer)
}

fn find_best_asteroid(asteroids: &Vec<Asteroid>) -> Option<(usize, Asteroid)> {
    if asteroids.len() == 0 {
        return None
    }
    let mut max_visible: usize = 0;
    let mut max_asteroid_index: usize = 0;
    for (index, asteroid) in asteroids.iter().enumerate() {
        let current_visible = asteroid.detect_asteroids(asteroids);
        if current_visible >= max_visible {
            max_visible = current_visible;
            max_asteroid_index = index;
        }
    }
    
    Some((max_visible, *asteroids.get(max_asteroid_index).unwrap()))
}

fn main() {
    let asteroids_result = read_aseroid_data("./data/input.in");
    match asteroids_result {
        Err(e) => panic!(e),
        Ok(asteroids) => {
            let best_asteroid = find_best_asteroid(&asteroids).unwrap();
            let vaportization_order = best_asteroid.1.vaporize_asteroids(&asteroids).unwrap();
            let last = vaportization_order.get(200).unwrap();
            println!("{:?} Answer={}", last, last.x * 100 + last.y);
        }
    };
}
