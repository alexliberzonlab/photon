# Autogenerated with SMOP version 
# /Users/lalit/anaconda/bin/smop mie_scattering_data.m

from __future__ import division
try:
    from runtime import *
except ImportError:
    from smop.runtime import *

def mie_scattering_data_(n_medium=None,n_particle=None,r_particle=None,lambda=None,angle_number=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 5-[n_medium,n_particle,r_particle,_lambda,angle_number].count(None)+len(args)

    n_particle_real=real_(n_particle)
    n_particle_imag=imag_(n_particle)
    n_medium_string=num2str_(n_medium,6)
    n_particle_real_string=num2str_(n_particle_real,6)
    n_particle_imag_string=num2str_(n_particle_imag,6)
    r_particle_string=num2str_(r_particle,6)
    lambda_string=num2str_(_lambda,6)
    angle_number_string=num2str_(angle_number)
    code_filename=mfilename_(char('fullpath'))
    truncate_index=strfind_(code_filename,filesep)
    truncate_index=truncate_index[end()] - 1
    code_directory=code_filename[1:truncate_index]
    table_filename=matlabarray([tempname,char('.out')])
    if exist_(table_filename,char('file')):
        delete_(table_filename)
    shell_command_string=matlabarray([char('cd '),code_directory,char('; ./bhmie_table '),n_medium_string,char(' '),n_particle_real_string,char(' '),n_particle_imag_string,char(' '),r_particle_string,char(' '),lambda_string,char(' '),angle_number_string,char(' > '),table_filename])
    system_(shell_command_string)
    load_attempt_number=0
    while true:

        if exist_(table_filename,char('file')):
            scattering_data=dlmread_(table_filename,char(''),5,0)
            break
        else:
            load_attempt_number=load_attempt_number + 1
            if load_attempt_number > 10:
                error_(char('The Mie scattering data has not be created and the maximum number of loading attempts for the data has been exceeded.'))
            pause_(0.1)

    delete_(table_filename)
    angle_data=scattering_data[:,1]
    angle_data=pi * angle_data / 180
    s11_data=scattering_data[:,2]
    pol_data=scattering_data[:,3]
    s12_data=- s11_data.dot(pol_data)
    s1_data=(s11_data - s12_data)
    s2_data=(s11_data + s12_data)
    return angle_data,s1_data,s2_data
