// Benchmark "div_rest" written by ABC on Thu Apr 27 11:26:25 2023

module div_rest ( 
    \X[0] , \X[1] , \X[2] , \X[3] , \X[4] , \D[0] , \D[1] , \D[2] ,
    \Q[0] , \Q[1] , \Q[2] , \R[0] , \R[1] , \R[2]   );
  input  \X[0] , \X[1] , \X[2] , \X[3] , \X[4] , \D[0] , \D[1] , \D[2] ;
  output \Q[0] , \Q[1] , \Q[2] , \R[0] , \R[1] , \R[2] ;
  wire new_n15_, new_n16_, new_n17_, new_n18_, new_n19_, new_n20_, new_n21_,
    new_n22_, new_n23_, new_n24_, new_n25_, new_n26_, new_n27_, new_n28_,
    new_n29_, new_n30_, new_n31_, new_n32_, new_n33_, new_n34_, new_n35_,
    new_n36_, new_n37_, new_n38_, new_n39_, new_n40_, new_n41_, new_n42_,
    new_n43_, new_n44_, new_n45_, new_n46_, new_n47_, new_n48_, new_n49_,
    new_n50_, new_n51_, new_n52_, new_n53_, new_n54_, new_n55_, new_n56_,
    new_n57_, new_n58_, new_n59_, new_n60_, new_n61_, new_n62_, new_n63_,
    new_n64_, new_n65_, new_n66_, new_n67_, new_n68_, new_n69_, new_n70_,
    new_n71_, new_n72_, new_n73_, new_n74_, new_n75_, new_n76_, new_n77_,
    new_n78_, new_n79_, new_n80_, new_n81_, new_n82_, new_n83_, new_n84_,
    new_n85_, new_n86_, new_n87_, new_n88_, new_n89_, new_n90_, new_n91_,
    new_n92_, new_n93_, new_n94_, new_n95_, new_n96_, new_n97_, new_n98_,
    new_n99_, new_n100_, new_n101_, new_n102_, new_n103_, new_n104_,
    new_n105_, new_n106_, new_n107_, new_n111_, new_n112_, new_n113_,
    new_n115_, new_n116_, new_n117_, new_n118_, new_n119_, new_n120_,
    new_n122_, new_n123_, new_n124_, new_n125_, new_n126_, new_n127_,
    new_n128_, new_n129_, new_n130_, new_n131_, new_n132_;
  nor3   g000(.a(\D[2] ), .b(\D[1] ), .c(\D[0] ), .O(new_n15_));
  inv1   g001(.a(new_n15_), .O(new_n16_));
  inv1   g002(.a(\D[1] ), .O(new_n17_));
  nor2   g003(.a(new_n17_), .b(\X[4] ), .O(new_n18_));
  inv1   g004(.a(\D[2] ), .O(new_n19_));
  nand2  g005(.a(new_n19_), .b(\D[0] ), .O(new_n20_));
  oai21  g006(.a(new_n20_), .b(new_n18_), .c(\X[3] ), .O(new_n21_));
  inv1   g007(.a(\X[2] ), .O(new_n22_));
  nand2  g008(.a(\D[0] ), .b(new_n22_), .O(new_n23_));
  nand2  g009(.a(new_n23_), .b(new_n17_), .O(new_n24_));
  nand2  g010(.a(new_n24_), .b(new_n21_), .O(new_n25_));
  inv1   g011(.a(new_n23_), .O(new_n26_));
  nand2  g012(.a(new_n26_), .b(\D[1] ), .O(new_n27_));
  nand3  g013(.a(new_n19_), .b(new_n17_), .c(\D[0] ), .O(new_n28_));
  nand2  g014(.a(new_n28_), .b(\X[4] ), .O(new_n29_));
  nand2  g015(.a(new_n29_), .b(\D[2] ), .O(new_n30_));
  nand3  g016(.a(new_n30_), .b(new_n27_), .c(new_n25_), .O(new_n31_));
  inv1   g017(.a(\X[3] ), .O(new_n32_));
  nand3  g018(.a(\D[1] ), .b(\D[0] ), .c(new_n32_), .O(new_n33_));
  inv1   g019(.a(\D[0] ), .O(new_n34_));
  oai21  g020(.a(new_n34_), .b(\X[3] ), .c(new_n17_), .O(new_n35_));
  nand2  g021(.a(new_n35_), .b(new_n33_), .O(new_n36_));
  nand4  g022(.a(new_n36_), .b(new_n28_), .c(new_n19_), .d(\X[4] ), .O(new_n37_));
  nand2  g023(.a(new_n37_), .b(new_n31_), .O(new_n38_));
  inv1   g024(.a(new_n38_), .O(new_n39_));
  nand2  g025(.a(new_n27_), .b(new_n24_), .O(new_n40_));
  nor2   g026(.a(new_n40_), .b(new_n39_), .O(new_n41_));
  xor2a  g027(.a(new_n41_), .b(new_n21_), .O(new_n42_));
  nor2   g028(.a(new_n34_), .b(\X[1] ), .O(new_n43_));
  inv1   g029(.a(new_n43_), .O(new_n44_));
  nand2  g030(.a(new_n38_), .b(new_n26_), .O(new_n45_));
  nand3  g031(.a(new_n28_), .b(new_n19_), .c(\X[4] ), .O(new_n46_));
  aoi21  g032(.a(new_n35_), .b(new_n33_), .c(new_n46_), .O(new_n47_));
  nand2  g033(.a(new_n21_), .b(\D[1] ), .O(new_n48_));
  aoi21  g034(.a(new_n48_), .b(new_n30_), .c(new_n47_), .O(new_n49_));
  oai21  g035(.a(new_n49_), .b(new_n34_), .c(\X[2] ), .O(new_n50_));
  aoi21  g036(.a(new_n50_), .b(new_n45_), .c(\D[1] ), .O(new_n51_));
  nand3  g037(.a(new_n50_), .b(new_n45_), .c(\D[1] ), .O(new_n52_));
  oai21  g038(.a(new_n51_), .b(new_n44_), .c(new_n52_), .O(new_n53_));
  aoi21  g039(.a(new_n53_), .b(\D[2] ), .c(new_n42_), .O(new_n54_));
  nand3  g040(.a(new_n27_), .b(new_n25_), .c(new_n19_), .O(new_n55_));
  nand2  g041(.a(new_n55_), .b(new_n38_), .O(new_n56_));
  inv1   g042(.a(new_n36_), .O(new_n57_));
  aoi21  g043(.a(new_n57_), .b(new_n19_), .c(new_n29_), .O(new_n58_));
  nand2  g044(.a(new_n58_), .b(new_n56_), .O(new_n59_));
  aoi21  g045(.a(new_n37_), .b(new_n31_), .c(new_n23_), .O(new_n60_));
  inv1   g046(.a(\X[4] ), .O(new_n61_));
  nand2  g047(.a(\D[1] ), .b(new_n61_), .O(new_n62_));
  nor2   g048(.a(\D[2] ), .b(new_n34_), .O(new_n63_));
  aoi21  g049(.a(new_n63_), .b(new_n62_), .c(new_n32_), .O(new_n64_));
  oai21  g050(.a(new_n64_), .b(new_n17_), .c(new_n30_), .O(new_n65_));
  nand2  g051(.a(new_n65_), .b(new_n37_), .O(new_n66_));
  aoi21  g052(.a(new_n66_), .b(\D[0] ), .c(new_n22_), .O(new_n67_));
  oai21  g053(.a(new_n67_), .b(new_n60_), .c(new_n17_), .O(new_n68_));
  nand2  g054(.a(new_n68_), .b(new_n43_), .O(new_n69_));
  nand3  g055(.a(new_n52_), .b(new_n69_), .c(new_n19_), .O(new_n70_));
  nand2  g056(.a(new_n70_), .b(new_n59_), .O(new_n71_));
  nand2  g057(.a(new_n52_), .b(new_n68_), .O(new_n72_));
  xor2a  g058(.a(new_n72_), .b(new_n43_), .O(new_n73_));
  oai21  g059(.a(new_n71_), .b(new_n54_), .c(new_n73_), .O(new_n74_));
  nand2  g060(.a(new_n50_), .b(new_n45_), .O(new_n75_));
  inv1   g061(.a(new_n42_), .O(new_n76_));
  nand2  g062(.a(new_n53_), .b(\D[2] ), .O(new_n77_));
  nand2  g063(.a(new_n77_), .b(new_n76_), .O(new_n78_));
  inv1   g064(.a(new_n52_), .O(new_n79_));
  aoi21  g065(.a(new_n68_), .b(new_n43_), .c(new_n79_), .O(new_n80_));
  inv1   g066(.a(new_n59_), .O(new_n81_));
  aoi21  g067(.a(new_n80_), .b(new_n19_), .c(new_n81_), .O(new_n82_));
  nand3  g068(.a(new_n82_), .b(new_n78_), .c(new_n75_), .O(new_n83_));
  nand3  g069(.a(new_n83_), .b(new_n74_), .c(\D[2] ), .O(new_n84_));
  nand2  g070(.a(new_n83_), .b(new_n74_), .O(new_n85_));
  nand4  g071(.a(new_n70_), .b(new_n81_), .c(new_n77_), .d(new_n42_), .O(new_n86_));
  nand2  g072(.a(new_n15_), .b(\X[4] ), .O(new_n87_));
  nand2  g073(.a(new_n70_), .b(new_n77_), .O(new_n88_));
  nand2  g074(.a(new_n88_), .b(new_n76_), .O(new_n89_));
  nor2   g075(.a(new_n34_), .b(\X[0] ), .O(new_n90_));
  nand4  g076(.a(new_n90_), .b(new_n89_), .c(new_n87_), .d(new_n86_), .O(new_n91_));
  aoi21  g077(.a(new_n85_), .b(new_n19_), .c(new_n91_), .O(new_n92_));
  oai21  g078(.a(new_n71_), .b(new_n54_), .c(\D[0] ), .O(new_n93_));
  xor2a  g079(.a(new_n93_), .b(\X[1] ), .O(new_n94_));
  nand2  g080(.a(new_n94_), .b(\D[1] ), .O(new_n95_));
  nand2  g081(.a(new_n82_), .b(new_n78_), .O(new_n96_));
  nand3  g082(.a(new_n96_), .b(\D[0] ), .c(\X[1] ), .O(new_n97_));
  inv1   g083(.a(\X[1] ), .O(new_n98_));
  nand2  g084(.a(new_n93_), .b(new_n98_), .O(new_n99_));
  nand3  g085(.a(new_n99_), .b(new_n97_), .c(new_n17_), .O(new_n100_));
  nand4  g086(.a(new_n100_), .b(new_n95_), .c(new_n92_), .d(new_n84_), .O(new_n101_));
  inv1   g087(.a(new_n84_), .O(new_n102_));
  aoi21  g088(.a(new_n99_), .b(new_n97_), .c(new_n17_), .O(new_n103_));
  nand3  g089(.a(new_n89_), .b(new_n87_), .c(new_n86_), .O(new_n104_));
  aoi21  g090(.a(new_n85_), .b(new_n19_), .c(new_n104_), .O(new_n105_));
  oai21  g091(.a(new_n103_), .b(new_n102_), .c(new_n105_), .O(new_n106_));
  nand3  g092(.a(new_n106_), .b(new_n101_), .c(new_n16_), .O(new_n107_));
  inv1   g093(.a(new_n107_), .O(\Q[0] ));
  aoi21  g094(.a(new_n82_), .b(new_n78_), .c(new_n15_), .O(\Q[1] ));
  nor2   g095(.a(new_n39_), .b(new_n15_), .O(\Q[2] ));
  nand3  g096(.a(new_n106_), .b(new_n101_), .c(new_n90_), .O(new_n111_));
  nand2  g097(.a(new_n106_), .b(\D[0] ), .O(new_n112_));
  nand2  g098(.a(new_n112_), .b(\X[0] ), .O(new_n113_));
  aoi21  g099(.a(new_n113_), .b(new_n111_), .c(new_n15_), .O(\R[0] ));
  inv1   g100(.a(new_n94_), .O(new_n115_));
  xor2a  g101(.a(new_n90_), .b(\D[1] ), .O(new_n116_));
  nand4  g102(.a(new_n116_), .b(new_n106_), .c(new_n101_), .d(new_n115_), .O(new_n117_));
  nand3  g103(.a(new_n116_), .b(new_n106_), .c(new_n101_), .O(new_n118_));
  nand2  g104(.a(new_n118_), .b(new_n94_), .O(new_n119_));
  nand3  g105(.a(new_n119_), .b(new_n117_), .c(new_n16_), .O(new_n120_));
  inv1   g106(.a(new_n120_), .O(\R[1] ));
  nand2  g107(.a(new_n106_), .b(new_n101_), .O(new_n122_));
  nand2  g108(.a(new_n85_), .b(new_n19_), .O(new_n123_));
  nand2  g109(.a(new_n100_), .b(new_n90_), .O(new_n124_));
  nand4  g110(.a(new_n124_), .b(new_n95_), .c(new_n123_), .d(new_n84_), .O(new_n125_));
  nand2  g111(.a(new_n124_), .b(new_n95_), .O(new_n126_));
  nand2  g112(.a(new_n123_), .b(new_n84_), .O(new_n127_));
  nand2  g113(.a(new_n127_), .b(new_n126_), .O(new_n128_));
  aoi21  g114(.a(new_n128_), .b(new_n125_), .c(new_n122_), .O(new_n129_));
  inv1   g115(.a(new_n85_), .O(new_n130_));
  nand2  g116(.a(new_n122_), .b(new_n130_), .O(new_n131_));
  nand2  g117(.a(new_n131_), .b(new_n16_), .O(new_n132_));
  nor2   g118(.a(new_n132_), .b(new_n129_), .O(\R[2] ));
endmodule


