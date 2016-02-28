# Autogenerated with SMOP version 
# /Users/lalit/anaconda/bin/smop run_piv_challenge_simulation_01.m

from __future__ import division
try:
    from runtime import *
except ImportError:
    from smop.runtime import *

def run_piv_challenge_simulation_01_(*args,**kwargs):
    varargin = cellarray(args)
    nargin = 0-[].count(None)+len(args)

    top_write_directory=char('/Users/lalit/Documents/PhD_Research/Projects/Ongoing/Computer_Generated_Schlieren/Software/pyCodes/camera_simulation/python_codes/test_directory/')
    camera_simulation_parameters_read_directory=char('/Users/lalit/Documents/PhD_Research/Projects/Ongoing/Computer_Generated_Schlieren/Software/pyCodes/camera_simulation/python_codes/piv_challenge_simulation_parameters/')
    camera_parameter_list=dir_([camera_simulation_parameters_read_directory,char('camera*.mat')])
    particle_image_top_directory=matlabarray([top_write_directory,char('camera_images/particle_images/')])
    if not_(exist_(particle_image_top_directory,char('dir'))):
        mkdir_(particle_image_top_directory)
    for camera_index in arange_(1,length_(camera_parameter_list)).reshape(-1):
        current_subdirectory=matlabarray([particle_image_top_directory,char('camera_'),sprintf_(char('%02.0f'),camera_index),char('/')])
        if not_(exist_(current_subdirectory,char('dir'))):
            mkdir_(current_subdirectory)
    calibration_image_top_directory=matlabarray([top_write_directory,char('camera_images/calibration_images/')])
    if not_(exist_(calibration_image_top_directory,char('dir'))):
        mkdir_(calibration_image_top_directory)
    for camera_index in arange_(1,length_(camera_parameter_list)).reshape(-1):
        current_subdirectory=matlabarray([calibration_image_top_directory,char('camera_'),sprintf_(char('%02.0f'),camera_index),char('/')])
        if not_(exist_(current_subdirectory,char('dir'))):
            mkdir_(current_subdirectory)
    X_Velocity=1000.0
    Y_Velocity=1000.0
    Z_Velocity=100.0
    X_Min=- 75000.0
    X_Max=+ 75000.0
    Y_Min=- 75000.0
    Y_Max=+ 75000.0
    Z_Min=- 7500.0
    Z_Max=+ 7500.0
    total_particle_number=10000000.0
    X=(X_Max - X_Min) * rand_(total_particle_number,1) + X_Min
    Y=(Y_Max - Y_Min) * rand_(total_particle_number,1) + Y_Min
    Z=(Z_Max - Z_Min) * rand_(total_particle_number,1) + Z_Min
    X1=X - X_Velocity / 2
    Y1=Y - Y_Velocity / 2
    Z1=Z - Z_Velocity / 2
    X2=X + X_Velocity / 2
    Y2=Y + Y_Velocity / 2
    Z2=Z + Z_Velocity / 2
    particle_position_data_directory=matlabarray([top_write_directory,char('particle_positions/')])
    if not_(exist_(particle_position_data_directory,char('dir'))):
        mkdir_(particle_position_data_directory)
    X=copy_(X1)
    Y=copy_(Y1)
    Z=copy_(Z1)
    save_([particle_position_data_directory,char('particle_data_frame_0001.mat')],char('X'),char('Y'),char('Z'))
    X=copy_(X2)
    Y=copy_(Y2)
    Z=copy_(Z2)
    save_([particle_position_data_directory,char('particle_data_frame_0002.mat')],char('X'),char('Y'),char('Z'))
    for camera_index in arange_(1,length_(camera_parameter_list)).reshape(-1):
        fprintf_(char('\\n\\n\\n\\n'))
        disp_([char('Running camera '),num2str_(camera_index),char(' simulation . . . ')])
        parameter_filename_read=matlabarray([camera_simulation_parameters_read_directory,camera_parameter_list[camera_index].name])
        load_(parameter_filename_read)
        piv_simulation_parameters.particle_field.data_directory=particle_position_data_directory
        piv_simulation_parameters.particle_field.frame_vector=arange_(1,2)
        piv_simulation_parameters.particle_field.particle_number=250000.0
        piv_simulation_parameters.output_data.particle_image_directory=[particle_image_top_directory,char('camera_'),sprintf_(char('%02.0f'),camera_index),char('/')]
        piv_simulation_parameters.output_data.calibration_grid_image_directory=[calibration_image_top_directory,char('camera_'),sprintf_(char('%02.0f'),camera_index),char('/')]
        run_piv_simulation_02_(piv_simulation_parameters)
    return
run_piv_challenge_simulation_01_()