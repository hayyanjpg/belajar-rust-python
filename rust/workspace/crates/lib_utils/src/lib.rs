/// Utilitas string untuk proyek belajar Rust
pub struct StringUtils;

impl StringUtils {
    /// Balikkan string
    pub fn reverse(s: &str) -> String {
        s.chars().rev().collect()
    }

    /// Hitung jumlah kata
    pub fn word_count(s: &str) -> usize {
        s.split_whitespace().count()
    }

    /// Ubah ke Title Case
    pub fn title_case(s: &str) -> String {
        s.split_whitespace()
            .map(|w| {
                let mut c = w.chars();
                match c.next() {
                    None => String::new(),
                    Some(f) => f.to_uppercase().collect::<String>() + c.as_str(),
                }
            })
            .collect::<Vec<_>>()
            .join(" ")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_reverse() {
        assert_eq!(StringUtils::reverse("hello"), "olleh");
        assert_eq!(StringUtils::reverse("rust"), "tsur");
    }

    #[test]
    fn test_word_count() {
        assert_eq!(StringUtils::word_count("hello world rust"), 3);
        assert_eq!(StringUtils::word_count(""), 0);
    }

    #[test]
    fn test_title_case() {
        assert_eq!(StringUtils::title_case("hello world"), "Hello World");
        assert_eq!(StringUtils::title_case("belajar rust"), "Belajar Rust");
    }
}
