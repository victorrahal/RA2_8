.global _start
.data
.align 3
val_1_0: .double 1.0
val_2_0: .double 2.0
val_3_0: .double 3.0
val_4_0: .double 4.0
val_5_0: .double 5.0
val_10_0: .double 10.0
resultado_0: .double 0.0
resultado_1: .double 0.0
resultado_2: .double 0.0
resultado_3: .double 0.0
resultado_4: .double 0.0
resultado_5: .double 0.0
resultado_6: .double 0.0
resultado_7: .double 0.0
resultado_8: .double 0.0
resultado_9: .double 0.0
resultado_10: .double 0.0
resultado_11: .double 0.0
resultado_12: .double 0.0
resultado_13: .double 0.0
resultado_14: .double 0.0
resultado_15: .double 0.0
resultado_16: .double 0.0
resultado_17: .double 0.0
resultado_18: .double 0.0
resultado_19: .double 0.0
.text
.arm
.fpu vfpv3
.align 2
_start:
    MOV R7, #1
    SWI #0
