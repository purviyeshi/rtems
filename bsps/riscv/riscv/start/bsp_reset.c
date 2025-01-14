/*
 * Copyright (c) 2018 embedded brains GmbH & Co. KG
 *
 * Copyright (c) 2015 University of York.
 * Hesham Almatary <hesham@alumni.york.ac.uk>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

#include <stdint.h>
#include <stdio.h>
#include <bsp/bsp_reset.h>
// #include <assert.h>
#include <bsp/reset.h>
#include <bsp/mss_sysreg.h>
// #include "/home/purva/quick-start/src/rtems/bsps/riscv/riscv/include/bsp/mss_sysreg.h"

__attribute__((__noreturn__)) static void HSS_reboot_cold_all(void)
{
    // Trigger a full MSS reset by writing 0xDEAD to the MSS_RESET_CR register.
    SYSREG->MSS_RESET_CR = 0xDEAD;

    // Print the value of SYSREG to check if it's correctly initialized
    printf("SYSREG pointer: %p\n", (void *)SYSREG);

    // Infinite loop to ensure the function does not return after the reset.
    while (1) { ; }
}


void HSS_reboot_cold(enum HSSHartId target)
{
    if (target == HSS_HART_ALL) {
        HSS_reboot_cold_all();
    } else {
        printf("Problem in Soft Reboot");
    }
}











