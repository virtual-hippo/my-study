// 参考: http://marupeke296.com/DP_AbstractFactory.html

// trait
trait AbstractWeapons {
    fn create_weapon(&self) -> Box<dyn AbstractWeapon>;
    fn create_bomb(&self) -> Box<dyn AbstractBomb>;
}


trait AbstractWeapon {
    fn get_type_name(&self) -> String;
}

trait AbstractBomb {
    fn get_type_name(&self) -> String;
}

trait AbstractMachine {
    fn create(&mut self, abs_wep: Box<dyn AbstractWeapons>);
}

// 実装
// product
struct Weapon1;
impl AbstractWeapon for Weapon1 {
    fn get_type_name(&self) -> String {
        "Weapon1".to_string()
    }
}

struct Bomb1;
impl AbstractBomb for Bomb1 {
    fn get_type_name(&self) -> String {
        "Bomb1".to_string()
    }
}

struct Weapon2;
impl AbstractWeapon for Weapon2 {
    fn get_type_name(&self) -> String {
        "Weapon2".to_string()
    }
}

struct Bomb2;
impl AbstractBomb for Bomb2 {
    fn get_type_name(&self) -> String {
        "Bomb2".to_string()
    }
}

// factory
pub struct AbstractWeaponsType1;
impl AbstractWeapons for AbstractWeaponsType1 {
    fn create_weapon(&self) -> Box<dyn AbstractWeapon> {
        Box::new(Weapon1) as Box<dyn AbstractWeapon>
    }
    fn create_bomb(&self) -> Box<dyn AbstractBomb> {
        Box::new(Bomb1) as Box<dyn AbstractBomb>
    }
}

pub struct AbstractWeaponsType2;
impl AbstractWeapons for AbstractWeaponsType2 {
    fn create_weapon(&self) -> Box<dyn AbstractWeapon> {
        Box::new(Weapon2) as Box<dyn AbstractWeapon>
    }
    fn create_bomb(&self) -> Box<dyn AbstractBomb> {
        Box::new(Bomb2) as Box<dyn AbstractBomb>
    }
}

// product owner
pub struct TypeMacine {
    weapon: Option<Box<dyn AbstractWeapon>>,
    bomb: Option<Box<dyn AbstractBomb>>,
}
impl AbstractMachine for TypeMacine {
    fn create(&mut self, abs_wep: Box<dyn AbstractWeapons>) {
        self.weapon = Some(abs_wep.create_weapon());
        self.bomb = Some(abs_wep.create_bomb());
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn type1() {
        let mut machine = Box::new(TypeMacine { weapon: None, bomb: None });
        let abs_wep1 = Box::new(AbstractWeaponsType1);
        machine.create(abs_wep1);
        if let Some(something) = machine.weapon {
            assert_eq!(something.get_type_name(), "Weapon1".to_string()); 
        }
        if let Some(something) = machine.bomb {
            assert_eq!(something.get_type_name(), "Bomb1".to_string()); 
        }
    }
    #[test]
    fn type2() {
        let mut machine = Box::new(TypeMacine { weapon: None, bomb: None });
        let abs_wep2 = Box::new(AbstractWeaponsType2);
        machine.create(abs_wep2);
        if let Some(something) = machine.weapon {
            assert_eq!(something.get_type_name(), "Weapon2".to_string()); 
        }
        if let Some(something) = machine.bomb {
            assert_eq!(something.get_type_name(), "Bomb2".to_string()); 
        }
    }
}