

/* Automatically generated HAL from HAL.xml */
/* NEVER EDIT MANUALLY */

/* Generated on: 2016-09-07 21:06:07 */

#ifndef __HAL_H__
#define __HAL_H__

#include <avr/io.h>

#define nop()                                    __asm__ __volatile__("nop")

/* MOSI -> PD7 (Output, Initially Inactive) */
#define MOSI_BIT                                 7
#define MOSI_PIN                                 PIND
#define MOSI_PORT                                PORTD
#define MOSI_DDR                                 DDRD
#define MOSI_ModeOutput()                        MOSI_DDR |= _BV(MOSI_BIT)
#define MOSI_IsOutput()                          ((MOSI_DDR & _BV(MOSI_BIT)) != 0)
#define MOSI_SetHIGH()                           MOSI_PORT |= _BV(MOSI_BIT)
#define MOSI_SetLOW()                            MOSI_PORT &= ~_BV(MOSI_BIT)
#define MOSI_Get()                               (MOSI_PIN & _BV(MOSI_BIT))
#define MOSI_SetInactive()                       MOSI_SetLOW()
#define MOSI_SetActive()                         MOSI_SetHIGH()
#define MOSI_Toggle()                            MOSI_PORT ^= _BV(MOSI_BIT)
#define MOSI_SetConditional(condition)           if (condition) MOSI_SetActive(); else MOSI_SetInactive()
#define MOSI_SetConditionalToggle(conditionon, conditionoff, conditiontoggle) if (conditionon) { MOSI_SetActive(); } else if (conditionoff) { MOSI_SetInactive(); } else if (conditiontoggle) { MOSI_Toggle(); }
#define MOSI_Pulse()                             { MOSI_SetActive(); MOSI_SetInactive(); }
#define MOSI_PulseNop()                          { MOSI_SetActive(); nop(); MOSI_SetInactive(); }
#define MOSI_IsInactive()                        (MOSI_Get() == 0)
#define MOSI_IsActive()                          (MOSI_Get() != 0)
#define MOSI_Init()                              { MOSI_SetInactive(); MOSI_ModeOutput(); }

/* SCK -> PD6 (Output, Initially Inactive) */
#define SCK_BIT                                  6
#define SCK_PIN                                  PIND
#define SCK_PORT                                 PORTD
#define SCK_DDR                                  DDRD
#define SCK_ModeOutput()                         SCK_DDR |= _BV(SCK_BIT)
#define SCK_IsOutput()                           ((SCK_DDR & _BV(SCK_BIT)) != 0)
#define SCK_SetHIGH()                            SCK_PORT |= _BV(SCK_BIT)
#define SCK_SetLOW()                             SCK_PORT &= ~_BV(SCK_BIT)
#define SCK_Get()                                (SCK_PIN & _BV(SCK_BIT))
#define SCK_SetInactive()                        SCK_SetLOW()
#define SCK_SetActive()                          SCK_SetHIGH()
#define SCK_Toggle()                             SCK_PORT ^= _BV(SCK_BIT)
#define SCK_SetConditional(condition)            if (condition) SCK_SetActive(); else SCK_SetInactive()
#define SCK_SetConditionalToggle(conditionon, conditionoff, conditiontoggle) if (conditionon) { SCK_SetActive(); } else if (conditionoff) { SCK_SetInactive(); } else if (conditiontoggle) { SCK_Toggle(); }
#define SCK_Pulse()                              { SCK_SetActive(); SCK_SetInactive(); }
#define SCK_PulseNop()                           { SCK_SetActive(); nop(); SCK_SetInactive(); }
#define SCK_IsInactive()                         (SCK_Get() == 0)
#define SCK_IsActive()                           (SCK_Get() != 0)
#define SCK_Init()                               { SCK_SetInactive(); SCK_ModeOutput(); }

/* CS -> PD5 (Output, Initially Inactive, Active-Low) */
#define CS_BIT                                   5
#define CS_PIN                                   PIND
#define CS_PORT                                  PORTD
#define CS_DDR                                   DDRD
#define CS_ModeOutput()                          CS_DDR |= _BV(CS_BIT)
#define CS_IsOutput()                            ((CS_DDR & _BV(CS_BIT)) != 0)
#define CS_SetHIGH()                             CS_PORT |= _BV(CS_BIT)
#define CS_SetLOW()                              CS_PORT &= ~_BV(CS_BIT)
#define CS_Get()                                 (CS_PIN & _BV(CS_BIT))
#define CS_SetInactive()                         CS_SetHIGH()
#define CS_SetActive()                           CS_SetLOW()
#define CS_Toggle()                              CS_PORT ^= _BV(CS_BIT)
#define CS_SetConditional(condition)             if (condition) CS_SetActive(); else CS_SetInactive()
#define CS_SetConditionalToggle(conditionon, conditionoff, conditiontoggle) if (conditionon) { CS_SetActive(); } else if (conditionoff) { CS_SetInactive(); } else if (conditiontoggle) { CS_Toggle(); }
#define CS_Pulse()                               { CS_SetActive(); CS_SetInactive(); }
#define CS_PulseNop()                            { CS_SetActive(); nop(); CS_SetInactive(); }
#define CS_IsInactive()                          (CS_Get() != 0)
#define CS_IsActive()                            (CS_Get() == 0)
#define CS_Init()                                { CS_SetInactive(); CS_ModeOutput(); }

/* SDA -> PC4 (Input/Output, Initially Input, Initially Pullup Off) */
#define SDA_BIT                                  4
#define SDA_PIN                                  PINC
#define SDA_PORT                                 PORTC
#define SDA_DDR                                  DDRC
#define SDA_SetPullupActive()                    SDA_PORT |= _BV(SDA_BIT)
#define SDA_SetPullupInactive()                  SDA_PORT &= ~_BV(SDA_BIT)
#define SDA_ModeInput()                          SDA_DDR &= ~_BV(SDA_BIT)
#define SDA_IsInput()                            ((SDA_DDR & _BV(SDA_BIT)) == 0)
#define SDA_Get()                                (SDA_PIN & _BV(SDA_BIT))
#define SDA_GetBit()                             (SDA_Get() >> SDA_BIT)
#define SDA_ModeOutput()                         SDA_DDR |= _BV(SDA_BIT)
#define SDA_IsOutput()                           ((SDA_DDR & _BV(SDA_BIT)) != 0)
#define SDA_SetHIGH()                            SDA_PORT |= _BV(SDA_BIT)
#define SDA_SetLOW()                             SDA_PORT &= ~_BV(SDA_BIT)
#define SDA_Get()                                (SDA_PIN & _BV(SDA_BIT))
#define SDA_SetInactive()                        SDA_SetLOW()
#define SDA_SetActive()                          SDA_SetHIGH()
#define SDA_Toggle()                             SDA_PORT ^= _BV(SDA_BIT)
#define SDA_SetConditional(condition)            if (condition) SDA_SetActive(); else SDA_SetInactive()
#define SDA_SetConditionalToggle(conditionon, conditionoff, conditiontoggle) if (conditionon) { SDA_SetActive(); } else if (conditionoff) { SDA_SetInactive(); } else if (conditiontoggle) { SDA_Toggle(); }
#define SDA_Pulse()                              { SDA_SetActive(); SDA_SetInactive(); }
#define SDA_PulseNop()                           { SDA_SetActive(); nop(); SDA_SetInactive(); }
#define SDA_IsInactive()                         (SDA_Get() == 0)
#define SDA_IsActive()                           (SDA_Get() != 0)
#define SDA_Init()                               { SDA_SetPullupInactive(); SDA_ModeInput(); }

/* SCL -> PC5 (Input/Output, Initially Input, Initially Pullup Off) */
#define SCL_BIT                                  5
#define SCL_PIN                                  PINC
#define SCL_PORT                                 PORTC
#define SCL_DDR                                  DDRC
#define SCL_SetPullupActive()                    SCL_PORT |= _BV(SCL_BIT)
#define SCL_SetPullupInactive()                  SCL_PORT &= ~_BV(SCL_BIT)
#define SCL_ModeInput()                          SCL_DDR &= ~_BV(SCL_BIT)
#define SCL_IsInput()                            ((SCL_DDR & _BV(SCL_BIT)) == 0)
#define SCL_Get()                                (SCL_PIN & _BV(SCL_BIT))
#define SCL_GetBit()                             (SCL_Get() >> SCL_BIT)
#define SCL_ModeOutput()                         SCL_DDR |= _BV(SCL_BIT)
#define SCL_IsOutput()                           ((SCL_DDR & _BV(SCL_BIT)) != 0)
#define SCL_SetHIGH()                            SCL_PORT |= _BV(SCL_BIT)
#define SCL_SetLOW()                             SCL_PORT &= ~_BV(SCL_BIT)
#define SCL_Get()                                (SCL_PIN & _BV(SCL_BIT))
#define SCL_SetInactive()                        SCL_SetLOW()
#define SCL_SetActive()                          SCL_SetHIGH()
#define SCL_Toggle()                             SCL_PORT ^= _BV(SCL_BIT)
#define SCL_SetConditional(condition)            if (condition) SCL_SetActive(); else SCL_SetInactive()
#define SCL_SetConditionalToggle(conditionon, conditionoff, conditiontoggle) if (conditionon) { SCL_SetActive(); } else if (conditionoff) { SCL_SetInactive(); } else if (conditiontoggle) { SCL_Toggle(); }
#define SCL_Pulse()                              { SCL_SetActive(); SCL_SetInactive(); }
#define SCL_PulseNop()                           { SCL_SetActive(); nop(); SCL_SetInactive(); }
#define SCL_IsInactive()                         (SCL_Get() == 0)
#define SCL_IsActive()                           (SCL_Get() != 0)
#define SCL_Init()                               { SCL_SetPullupInactive(); SCL_ModeInput(); }

#define initHAL() {\
		MOSI_Init();\
		SCK_Init();\
		CS_Init();\
		SDA_Init();\
		SCL_Init();\
}

#endif
