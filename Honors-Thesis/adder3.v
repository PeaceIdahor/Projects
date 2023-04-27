// Benchmark "ADD3" written by ABC on Fri Apr 21 14:16:31 2023

module ADD3 ( 
    a0, a1, a2, b0, b1, b2,
    s0, s1, s2, s3  );
  input  a0, a1, a2, b0, b1, b2;
  output s0, s1, s2, s3;
  wire new_n11_, new_n12_, new_n13_, new_n15_, new_n17_, new_n18_, new_n19_,
    new_n20_, new_n22_, new_n23_;
  nand2  g00(.a(b0), .b(a0), .O(new_n11_));
  inv1   g01(.a(new_n11_), .O(new_n12_));
  nor2   g02(.a(b0), .b(a0), .O(new_n13_));
  nor2   g03(.a(new_n13_), .b(new_n12_), .O(s0));
  xor2a  g04(.a(b1), .b(a1), .O(new_n15_));
  xor2a  g05(.a(new_n15_), .b(new_n12_), .O(s1));
  nand2  g06(.a(b1), .b(a1), .O(new_n17_));
  nor2   g07(.a(b1), .b(a1), .O(new_n18_));
  oai21  g08(.a(new_n18_), .b(new_n11_), .c(new_n17_), .O(new_n19_));
  xor2a  g09(.a(b2), .b(a2), .O(new_n20_));
  xor2a  g10(.a(new_n20_), .b(new_n19_), .O(s2));
  nand2  g11(.a(b2), .b(a2), .O(new_n22_));
  nand2  g12(.a(new_n20_), .b(new_n19_), .O(new_n23_));
  nand2  g13(.a(new_n23_), .b(new_n22_), .O(s3));
endmodule


