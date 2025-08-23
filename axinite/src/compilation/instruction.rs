pub enum InstructionType {
    Const(f64, usize), // value, target
    Var(String, usize), // name, target
    Add(usize, usize, usize), // src 1 & 2, dest
    Multiply(usize, usize, usize), // src 1 & 2, dest
    Vec3(usize, usize, usize) // src 1 & 2, dest
}

pub struct Instruction {
    inst_type: InstructionType,
    operands: Vec<f64>,
    target: String
}