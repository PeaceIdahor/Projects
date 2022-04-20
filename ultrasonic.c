#define F_CPU 16000000
#define TRIGGER 1
#include <avr/io.h>
#include <util/delay.h>
#include <string.h>
#include <stdlib.h>
#include <avr/interrupt.h>
#define DIG1 3
#define DIG2 2
#define DIG3 1
#define DIG4 0
void usart_init(void);
void sart_send(unsigned char);
void send_string(char *stringAddress);




int main(void)
{
        unsigned char i, ledDigits[] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D,
        0x07, 0x7F, 0x67};
        unsigned char numRepeats = 200, persistence = 5;
        DDRC = (1 << DIG1) | (1 << DIG2) | (1 << DIG3) | (1 << DIG4);
        char buffer[10];
        float distance;
        unsigned int timeToRisingEdge, timeToFallingEdge, pulseWidth;
        DDRB = 1 << TRIGGER; //set PC0 as an output pin
        DDRD = 0xFF;
        usart_init();
        TCCR1A = 0; //timer 1
        DDRC = (1<<5);
        TCCR0A = 0x00;
        TCCR1B = 5;
        TCCR2A = 0x00;
        TCCR2B = 0x05;
        TCNT2 = 0;
        TIMSK2 = (1<<TOIE2);
        sei();
        
        while (1) {
                
                PORTB |= 1 << TRIGGER; //provide a 10.0 us pulse to
                _delay_us(10.);                        //to the
                PORTB &= ~(1 << TRIGGER); //trigger pin for the sonar
                TCNT1 = 0x00;
                
                TCCR1B = 0x45;
                while ((TIFR1 & (1 << ICF1)) == 0); 
                timeToRisingEdge = ICR1;
                TIFR1 = (1 << ICF1);
                TCCR1B = 0x05;
                while ((TIFR1 & (1 << ICF1)) == 0);
                timeToFallingEdge = ICR1;
                TIFR1 = (1 << ICF1);
                utoa(timeToRisingEdge, buffer, 10);
                send_string(buffer);
                usart_send(' ');
                utoa(timeToFallingEdge, buffer, 10);
                send_string(buffer);
                usart_send(' ');
                pulseWidth = timeToFallingEdge - timeToRisingEdge;
                distance = pulseWidth * 1.098;
                utoa(pulseWidth, buffer, 10);
                send_string(buffer);
                usart_send(' ');
                dtostrf(distance, 5, 1, buffer); // send distance in cm
                send_string(buffer);
                usart_send(' ');
                dtostrf(distance / 2.54, 5, 1, buffer); //send distance in inches to uart
                send_string(buffer);
                usart_send(13);
                usart_send(10);
                _delay_ms(250);
                //display output in cm on digital clock
                int cmDistance = distance;
                if((distance > 0) & (distance < 300)) {
                        for(i=0; i<numRepeats; i++){
                                PORTD = ledDigits[cmDistance/100];
                                PORTC = (1 << DIG1) | (1 << DIG2) | (1 << DIG4); //hundreds
                                _delay_ms(persistence);
                                PORTD = ledDigits[cmDistance/10%10];
                                PORTC = (1 << DIG1) | (1 << DIG3) | (1 << DIG4); //tens place
                                _delay_ms(persistence);
                                PORTD = ledDigits[cmDistance%10];
                                PORTC = (1 << DIG2) | (1 << DIG3) | (1 << DIG4); //ones place
                                _delay_ms(persistence);
                        }
                        
                }
        }
        }


void usart_init(void)
{
        UCSR0B = (1 << TXEN0);
        UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
        UBRR0L = 103;
}
void usart_send(unsigned char ch)
{
        while (!(UCSR0A & (1 << UDRE0)));
        UDR0 = ch;
}
void send_string(char *stringAddress)
{
        unsigned char i;
        for (i=0; i < strlen(stringAddress); i++)
        usart_send(stringAddress[i]);
}