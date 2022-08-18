`timescale 100 ps/10 ps

// The `timescale directive specifies that
// the simulation time unit is 100 ps and
// the simulator timestep is 10 ps

module rle_testbench;
	// signal declaration
	reg clkt, rstt; //input signalsv
	reg recv_readyt, send_readyt;
	reg [7:0] in_datat;
	reg end_of_streamt;
	wire [23:0] out_datat;
	wire rd_reqt, wr_reqt;

	// instantiate the circuit under test
	rle_enc uut
		(.clk(clkt), .rst(rstt), .recv_ready(recv_readyt), .send_ready(send_readyt), .in_data(in_datat), .end_of_stream(end_of_streamt), .out_data(out_datat), .rd_req(rd_reqt), .wr_req(wr_reqt));


	// clock running forever
	initial
	begin
		clkt=1'b0;
	end

	always #1 clkt = ~clkt;
	// reset for a few cycles
	initial
	begin
		fork
			recv_readyt <= 1'b1; //set inside side of FIFO to not empty
			send_readyt <= 1'b1; //outside side of FIFO is not full
			end_of_streamt <= 1'b0; //indicate end of bitstream has not been encountered
		join
		//#1 rstt = 1'b1; //reset the clock to 
		//#2 rstt = 1'b0;
	end

	// test vector generator
	initial begin
		#1 in_datat[7:0] <= 8'b11111111; //sending the data for vector 1 into the input side of FIFO
		#2 recv_readyt <= 1'b1; // the input side FIFO is full
		#2 recv_readyt <= 1'b0;
		#2 end_of_streamt <= 1'b1;
		#2 end_of_streamt <= 1'b0;
		#50 in_datat[7:0] <= 8'b00000000; //sending data for vector 2 into the input side of the FIFO
		#2 recv_readyt <= 1'b1;
		#2 recv_readyt <= 1'b0;
		#2 end_of_streamt <= 1'b1;
		#2 end_of_streamt <= 1'b0;
		#50 in_datat[7:0] <= 8'b00011100; ////sending the data for vector 3 into the input side of the FIFO
		#2 recv_readyt <= 1'b1;
		#2 recv_readyt <= 1'b0;
		//#2 end_of_streamt <= 1'b1;
		/*
		#50 in_datat[7:0] <= 8'b10101010;
		#2 recv_readyt <=1'b1;
		#2 recv_readyt <=1'b0;
		#2 end_of_streamt <= 1'b1;
		#50 in_datat[7:0] <= 8'b00000001;
		#2 recv_readyt <= 1'b1;
		#2 recv_readyt <= 1'b0;*/
		

		$stop;
	end
endmodule
