################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CU_SRCS += \
../distortion_correction.cu 

OBJS += \
./distortion_correction.o 

CU_DEPS += \
./distortion_correction.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cu
	@echo 'Building file: $<'
	@echo 'Invoking: NVCC Compiler'
	/usr/local/cuda-8.0/bin/nvcc -I/usr/include/opencv -G -g -O0 -gencode arch=compute_30,code=sm_30 -gencode arch=compute_32,code=sm_32  -odir "." -M -o "$(@:%.o=%.d)" "$<"
	/usr/local/cuda-8.0/bin/nvcc -I/usr/include/opencv -G -g -O0 --compile --relocatable-device-code=false -gencode arch=compute_30,code=compute_30 -gencode arch=compute_32,code=sm_32  -x cu -o  "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


