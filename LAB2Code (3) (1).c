/*Peace Idahor
Lab 2 Code
*/
#include <avr/io.h>
#define F_CPU 16000000UL
#include <util/delay.h>
#include <string.h> //to use the strlen()
#include <stdlib.h> //to use itoa()
#define DIG4 3 //B3, enables DIG4
#define DIG3 2 //B2, enables DIG3
#define DIG2 1 //B1, enables DIG2
#define DIG1 0 //B0, enables DIG1
#define TempSwitch 1 // switch for the temp PC1
#define sensor 0 // sensor
//void uart_init(void);
//void uart_send(char letter);
//void send_string(char*stringAddress);
void DisplayTemp(char *Num,char U);
void ShowDIG(char digit);
int main(void)
{
	unsigned int digitalValue;
	int voltInt;
	int voltIntC;
	int voltIntF;
	char buffer[3];
	DDRD = 0xFF;//setting all the pins to outputs
	DDRB = (1 << DIG4) | (1 << DIG3) |(1 << DIG2) | (1 << DIG1); //digit enables
	DDRC &= ~(1<<sensor); //PC0 as input
	DDRC &=~(1<<TempSwitch); //PC1 as input
	PORTC |= (1<<TempSwitch); //setting Portc as the input to the switch
	ADCSRA = 0x87;
	ADMUX =0xC0 ; // 0110 0000 ADC0, Vref=AVCC=1.1V;

	//uart_init();
	while(1){
		ADCSRA |= (1<<ADSC) ;
		while ((ADCSRA & (1<<ADIF))==0);
		digitalValue = ADCL | (ADCH <<8); //read ADCL first
		//send_string(buffer);//txt string
		voltInt = digitalValue*1.1/1.024; // converting from the data from the sensor
		if((PINC &(1<<TempSwitch))==0){
			voltIntF = ((voltInt -500)*9)/5 +320; // temp in Fahrenheit
			itoa(voltIntF, buffer,10);//convert to character string 
			DisplayTemp(buffer,'F'); // utilizing the display function I made as well as making sure the function knows it's in Fahrenheit
		}
		else{
			voltIntC = (voltInt - 500); //temp in c
			itoa(voltIntC, buffer,10);//convert to character string 
			DisplayTemp(buffer,'C'); // utilizing the display function I made as well as making sure the function knows it's in Celsius
		}

		}
	}

//----------------------- Functions------------------------------
void ShowDIG(char digit){ //to display single digits
	unsigned char LEDDigit[]= {0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67,0x80,0x71, 0x39};
		PORTD = LEDDigit[digit];
		_delay_ms(1); //led is on for 1 ms
		PORTD= 0x00;
}
void DisplayTemp(char *Num,char U){//I added a unit parameter to specify F or C
	unsigned char i,j;
	unsigned char numReapeat = 100; //refresh rate of the digit
	PORTB =0xFF; //all coms pins stay high at the beginning -- disabling DIG1-4
	for (j=0;j<numReapeat;j++){
		for(i=0;i<4;i++){
			PORTB &=~(1<<(3-i)); //select digit position
			ShowDIG(Num[i] -'0'); //need to minus '0' or we are working with ASCII
			if(i==1) //when the second digit is enabled
				ShowDIG(10); //To show the decimal point
			PORTB |=0xFF; //disabling all digits so it shows one at a time
			}
			//----------Code to implement units----------
			if (U == 'C'){// if it is in C
				PORTB &= ~(1<<DIG1);
				ShowDIG(11);//i put 11 because the hex for C is in index 11 in my LEDDigits array
				PORTB |=0xFF;
			}
				
			if (U == 'F'){// if it is in F
				PORTB &=~(1<<DIG1);
				ShowDIG(12);//i put 12 because the hex for F is in index 12 in my LEDDigits array
				PORTB |=0xFF;
			
			}
		}
}
