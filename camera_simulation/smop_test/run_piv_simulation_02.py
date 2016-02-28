# Autogenerated with SMOP version 
# /Users/lalit/anaconda/bin/smop run_piv_simulation_02.m

from __future__ import division
try:
    from runtime import *
except ImportError:
    from smop.runtime import *

def run_piv_simulation_02_(piv_simulation_parameters=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 1-[piv_simulation_parameters].count(None)+len(args)

    optical_system=create_camera_optical_system_(piv_simulation_parameters)
    generate_particle_field_images=piv_simulation_parameters.particle_field.generate_particle_field_images
    frame_vector=piv_simulation_parameters.particle_field.frame_vector
    particle_image_directory=piv_simulation_parameters.output_data.particle_image_directory
    lightray_number_per_particle=piv_simulation_parameters.particle_field.lightray_number_per_particle
    lightray_process_number=piv_simulation_parameters.particle_field.lightray_process_number
    pixel_gain=piv_simulation_parameters.particle_field.pixel_gain
    perform_mie_scattering=piv_simulation_parameters.particle_field.perform_mie_scattering
    if generate_particle_field_images:
        fprintf_(char('\\n\\n'))
        disp_(char('Simulating particle images . . . '))
        if perform_mie_scattering:
            scattering_data=create_mie_scattering_data_(piv_simulation_parameters)
            scattering_type=char('mie')
        else:
            scattering_data=matlabarray([])
            scattering_type=char('diffuse')
        for frame_index in frame_vector.reshape(-1):
            lightfield_source=load_lightfield_data_(piv_simulation_parameters,optical_system,scattering_data,frame_index)
            lightfield_source.lightray_number_per_particle=lightray_number_per_particle
            lightfield_source.lightray_process_number=lightray_process_number
            I=perform_ray_tracing_03_(piv_simulation_parameters,optical_system,pixel_gain,scattering_data,scattering_type,lightfield_source)
            image_filename_write=matlabarray([particle_image_directory,char('particle_image_frame_'),sprintf_(char('%04.0f'),frame_index),char('.tif')])
            imwrite_(I,image_filename_write,char('tif'),char('Compression'),char('none'))
    generate_calibration_grid_images=piv_simulation_parameters.calibration_grid.generate_calibration_grid_images
    calibration_plane_number=piv_simulation_parameters.calibration_grid.calibration_plane_number
    calibration_grid_image_directory=piv_simulation_parameters.output_data.calibration_grid_image_directory
    lightray_number_per_particle=piv_simulation_parameters.calibration_grid.lightray_number_per_particle
    lightray_process_number=piv_simulation_parameters.calibration_grid.lightray_process_number
    pixel_gain=piv_simulation_parameters.calibration_grid.pixel_gain
    if generate_calibration_grid_images:
        fprintf_(char('\\n\\n'))
        disp_(char('Simulating calibration images . . . '))
        scattering_type=char('diffuse')
        scattering_data=matlabarray([])
        for plane_index in arange_(1,calibration_plane_number).reshape(-1):
            lightfield_source=generate_calibration_lightfield_data_(piv_simulation_parameters,optical_system,plane_index)
            lightfield_source.lightray_number_per_particle=lightray_number_per_particle
            lightfield_source.lightray_process_number=lightray_process_number
            I=perform_ray_tracing_03_(piv_simulation_parameters,optical_system,pixel_gain,scattering_data,scattering_type,lightfield_source)
            image_filename_write=matlabarray([calibration_grid_image_directory,char('calibration_image_plane_'),sprintf_(char('%04.0f'),plane_index),char('.tif')])
            imwrite_(I,image_filename_write,char('tif'),char('Compression'),char('none'))
    return
def create_mie_scattering_data_(piv_simulation_parameters=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 1-[piv_simulation_parameters].count(None)+len(args)

    x_camera_angle=piv_simulation_parameters.camera_design.x_camera_angle
    y_camera_angle=piv_simulation_parameters.camera_design.y_camera_angle
    beam_propogation_vector=piv_simulation_parameters.particle_field.beam_propogation_vector
    particle_diameter_vector,particle_diameter_pdf=calculate_particle_diameter_distribution_(piv_simulation_parameters,nargout=2)
    particle_diameter_index_distribution=calculate_particle_diameter_indices_(piv_simulation_parameters,particle_diameter_pdf,particle_diameter_vector)
    scattering_angle,scattering_irradiance=calculate_mie_scattering_intensity_(piv_simulation_parameters,particle_diameter_vector,nargout=2)
    rotation_matrix=calculate_rotation_matrix_(x_camera_angle,y_camera_angle,0)
    inverse_rotation_matrix=rotation_matrix.T
    beam_propogation_vector=beam_propogation_vector / norm_(beam_propogation_vector)
    mie_scattering_data=copy_(struct)
    mie_scattering_data.particle_diameter_vector=particle_diameter_vector
    mie_scattering_data.particle_diameter_pdf=particle_diameter_pdf
    mie_scattering_data.particle_diameter_index_distribution=particle_diameter_index_distribution
    mie_scattering_data.scattering_angle=scattering_angle
    mie_scattering_data.scattering_irradiance=scattering_irradiance
    mie_scattering_data.inverse_rotation_matrix=inverse_rotation_matrix
    mie_scattering_data.beam_propogation_vector=beam_propogation_vector
    return mie_scattering_data
def calculate_mie_scattering_intensity_(piv_simulation_parameters=None,particle_diameter_vector=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 2-[piv_simulation_parameters,particle_diameter_vector].count(None)+len(args)

    medium_refractive_index=piv_simulation_parameters.particle_field.medium_refractive_index
    particle_refractive_index=piv_simulation_parameters.particle_field.particle_refractive_index
    mie_scattering_angle_number=piv_simulation_parameters.particle_field.mie_scattering_angle_number
    beam_wavelength=piv_simulation_parameters.particle_field.beam_wavelength
    scattering_irradiance=zeros_(2 * mie_scattering_angle_number - 1,length_(particle_diameter_vector))
    for particle_diameter_index in arange_(1,length_(particle_diameter_vector)).reshape(-1):
        current_particle_radius=particle_diameter_vector[particle_diameter_index]
        scattering_angle,perpendicular_scattering_irradiance,parallel_scattering_irradiance=mie_scattering_data_(medium_refractive_index,particle_refractive_index,current_particle_radius,beam_wavelength,mie_scattering_angle_number,nargout=3)
        scattering_irradiance[:,particle_diameter_index]=0.5 * perpendicular_scattering_irradiance + 0.5 * parallel_scattering_irradiance
    return scattering_angle,scattering_irradiance
def calculate_particle_diameter_distribution_(piv_simulation_parameters=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 1-[piv_simulation_parameters].count(None)+len(args)

    particle_diameter_mean=piv_simulation_parameters.particle_field.particle_diameter_mean
    particle_diameter_std=piv_simulation_parameters.particle_field.particle_diameter_std
    particle_diameter_number=piv_simulation_parameters.particle_field.particle_diameter_number
    particle_diameter_cdf_threshhold=piv_simulation_parameters.particle_field.particle_diameter_cdf_threshhold
    particle_diameter_mu=log_(particle_diameter_mean) - (1 / 2) * log_(1 + (particle_diameter_std / particle_diameter_mean) ** 2)
    particle_diameter_sigma=sqrt_(log_(1 + (particle_diameter_std / particle_diameter_mean) ** 2))
    minimum_particle_diameter,maximum_particle_diameter=calculate_log_normal_pdf_extrema_(particle_diameter_mu,particle_diameter_sigma,particle_diameter_cdf_threshhold,nargout=2)
    particle_diameter_spacing=(maximum_particle_diameter - minimum_particle_diameter) / particle_diameter_number
    particle_diameter_vector=minimum_particle_diameter + particle_diameter_spacing * ((arange_(0,(particle_diameter_number - 1))) + 0.5)
    particle_diameter_pdf=log_normal_pdf_(particle_diameter_vector,particle_diameter_mu,particle_diameter_sigma)
    particle_diameter_pdf=particle_diameter_pdf / sum_(particle_diameter_pdf)
    return particle_diameter_vector,particle_diameter_pdf
def calculate_particle_diameter_indices_(piv_simulation_parameters=None,particle_diameter_pdf=None,particle_diameter_vector=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 3-[piv_simulation_parameters,particle_diameter_pdf,particle_diameter_vector].count(None)+len(args)

    particle_number=piv_simulation_parameters.particle_field.particle_number
    particle_diameter_cdf=cumsum_(particle_diameter_pdf)
    particle_diameter_cdf=matlabarray([0,particle_diameter_cdf])
    random_vector=rand_(particle_number,1)
    particle_diameter_index_distribution=zeros_(particle_number,1)
    for particle_diameter_index in arange_(1,length_(particle_diameter_vector)).reshape(-1):
        diameter_indices=(particle_diameter_cdf[particle_diameter_index] <= random_vector) and (random_vector < particle_diameter_cdf[particle_diameter_index + 1])
        particle_diameter_index_distribution[diameter_indices]=particle_diameter_index
    return particle_diameter_index_distribution
def calculate_log_normal_pdf_extrema_(mu=None,sigma=None,t=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 3-[mu,sigma,t].count(None)+len(args)

    x_max=exp_(mu + sigma)
    while true:

        y=log_normal_pdf_(x_max,mu,sigma)
        x_min,x_max=inverse_log_normal_pdf_(y,mu,sigma,nargout=2)
        dx=(1 - (log_normal_cdf_(x_max,mu,sigma) - log_normal_cdf_(x_min,mu,sigma)) - t) / (log_normal_pdf_(x_min,mu,sigma) * (- exp_(2 * mu - 2 * sigma ** 2) / (x_max ** 2)) - log_normal_pdf_(x_max,mu,sigma))
        if abs_(dx) < (eps_(mu) * 100.0):
            break
        x_max=x_max - dx

    return x_min,x_max
def log_normal_pdf_(x=None,mu=None,sigma=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 3-[x,mu,sigma].count(None)+len(args)

    y=(1.0 / (x.dot(sigma) * sqrt_(2 * pi))).dot(exp_(- ((log_(x) - mu) ** 2) / (2 * sigma ** 2)))
    return y
def inverse_log_normal_pdf_(y=None,mu=None,sigma=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 3-[y,mu,sigma].count(None)+len(args)

    x1=exp_(mu - sigma ** 2 - sigma.dot(sqrt_(sigma ** 2 - 2 * mu - 2 * log_(y.dot(sigma) * sqrt_(2 * pi)))))
    x2=exp_(mu - sigma ** 2 + sigma.dot(sqrt_(sigma ** 2 - 2 * mu - 2 * log_(y.dot(sigma) * sqrt_(2 * pi)))))
    return x1,x2
def log_normal_cdf_(x=None,mu=None,sigma=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 3-[x,mu,sigma].count(None)+len(args)

    y=(1 + erf_((log_(x) - mu) / (sigma * sqrt_(2)))) / 2
    return y
def generate_calibration_lightfield_data_(piv_simulation_parameters=None,optical_system=None,plane_index=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 3-[piv_simulation_parameters,optical_system,plane_index].count(None)+len(args)

    object_distance=piv_simulation_parameters.lens_design.object_distance
    focal_length=piv_simulation_parameters.lens_design.focal_length
    calibration_plane_spacing=piv_simulation_parameters.calibration_grid.calibration_plane_spacing
    calibration_plane_number=piv_simulation_parameters.calibration_grid.calibration_plane_number
    grid_point_diameter=piv_simulation_parameters.calibration_grid.grid_point_diameter
    x_grid_point_spacing=piv_simulation_parameters.calibration_grid.x_grid_point_spacing
    y_grid_point_spacing=piv_simulation_parameters.calibration_grid.y_grid_point_spacing
    x_grid_point_number=piv_simulation_parameters.calibration_grid.x_grid_point_number
    y_grid_point_number=piv_simulation_parameters.calibration_grid.y_grid_point_number
    particle_number_per_grid_point=piv_simulation_parameters.calibration_grid.particle_number_per_grid_point
    x_camera_angle=piv_simulation_parameters.camera_design.x_camera_angle
    y_camera_angle=piv_simulation_parameters.camera_design.y_camera_angle
    refractive_index=optical_system.design.optical_element.optical_element.element_properties.refractive_index
    front_surface_radius=optical_system.design.optical_element.optical_element.element_geometry.front_surface_radius
    back_surface_radius=optical_system.design.optical_element.optical_element.element_geometry.back_surface_radius
    optical_system_length=optical_system.design.optical_element.optical_element.element_geometry.vertex_distance
    image_distance=(1 / focal_length - 1 / object_distance) ** - 1
    h1_principal_plane=- (focal_length * (refractive_index - 1) * optical_system_length) / (back_surface_radius * refractive_index)
    h2_principal_plane=- (focal_length * (refractive_index - 1) * optical_system_length) / (front_surface_radius * refractive_index)
    v2_vertex_plane=image_distance + h2_principal_plane
    v1_vertex_plane=v2_vertex_plane + optical_system_length
    z_object=v1_vertex_plane - h1_principal_plane + object_distance
    grid_plane_z_world_coordinate=calibration_plane_spacing * (arange_(- (calibration_plane_number - 1) / 2,(calibration_plane_number - 1) / 2,1))
    current_z_world_coordinate=grid_plane_z_world_coordinate[plane_index]
    x_grid_point_coordinate_vector=x_grid_point_spacing * (arange_(- (x_grid_point_number - 1) / 2,(x_grid_point_number - 1) / 2,1))
    y_grid_point_coordinate_vector=y_grid_point_spacing * (arange_(- (y_grid_point_number - 1) / 2,(y_grid_point_number - 1) / 2,1))
    x_lightray_coordinates,y_lightray_coordinates=calculate_sunflower_coordinates_(grid_point_diameter,particle_number_per_grid_point,nargout=2)
    x=zeros_(particle_number_per_grid_point * x_grid_point_number * y_grid_point_number,1)
    y=zeros_(particle_number_per_grid_point * x_grid_point_number * y_grid_point_number,1)
    count=0
    for x_grid_index in arange_(1,x_grid_point_number).reshape(-1):
        for y_grid_index in arange_(1,y_grid_point_number).reshape(-1):
            x_grid_point_coordinate=x_grid_point_coordinate_vector[x_grid_index]
            y_grid_point_coordinate=y_grid_point_coordinate_vector[y_grid_index]
            x_grid_point_lightray_coordinates=x_lightray_coordinates + x_grid_point_coordinate
            y_grid_point_lightray_coordinates=y_lightray_coordinates + y_grid_point_coordinate
            index_vector=(count + 1) + (arange_(1,length_(x_grid_point_lightray_coordinates)))
            count=count + length_(x_grid_point_lightray_coordinates)
            x[index_vector]=x_grid_point_lightray_coordinates
            y[index_vector]=y_grid_point_lightray_coordinates
    if (count + 1) < length_(x):
        x[count + 1:end()]=[]
        y[count + 1:end()]=[]
    x_lightray_coordinates,y_lightray_coordinates=calculate_sunflower_coordinates_(grid_point_diameter / 4,particle_number_per_grid_point / 16,nargout=2)
    x_grid_point_coordinate=- x_grid_point_spacing / 2
    y_grid_point_coordinate=0
    x_grid_point_lightray_coordinates=x_lightray_coordinates + x_grid_point_coordinate
    y_grid_point_lightray_coordinates=y_lightray_coordinates + y_grid_point_coordinate
    x=matlabarray([[x],[x_grid_point_lightray_coordinates]])
    y=matlabarray([[y],[y_grid_point_lightray_coordinates]])
    x_grid_point_coordinate=0
    y_grid_point_coordinate=y_grid_point_spacing / 2
    x_grid_point_lightray_coordinates=x_lightray_coordinates + x_grid_point_coordinate
    y_grid_point_lightray_coordinates=y_lightray_coordinates + y_grid_point_coordinate
    x=matlabarray([[x],[x_grid_point_lightray_coordinates]])
    y=matlabarray([[y],[y_grid_point_lightray_coordinates]])
    z=current_z_world_coordinate * ones_(size_(x))
    radiance=ones_(size_(x))
    x,y,z=rotate_coordinates_(x,y,z,x_camera_angle,y_camera_angle,0,0,0,0,nargout=3)
    z=z + z_object
    lightfield_source.x=x
    lightfield_source.y=y
    lightfield_source.z=z
    lightfield_source.radiance=radiance
    lightfield_source.diameter_index=ones_(size_(x))
    return lightfield_source
def calculate_sunflower_coordinates_(grid_point_diameter=None,lightray_number_per_grid_point=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 2-[grid_point_diameter,lightray_number_per_grid_point].count(None)+len(args)

    grid_point_area=pi * (grid_point_diameter / 2) ** 2
    lightray_point_spacing=sqrt_(grid_point_area / lightray_number_per_grid_point)
    radius_lightray_vector=linspace_(lightray_point_spacing,(grid_point_diameter / 2),round_((grid_point_diameter / 2) / lightray_point_spacing))
    rho=1 / lightray_point_spacing
    x_lightray_coordinates=matlabarray([])
    y_lightray_coordinates=matlabarray([])
    for n in arange_(1,length_(radius_lightray_vector)).reshape(-1):
        radius_current=radius_lightray_vector[n]
        circle_lightray_point_number=round_(rho * (2 * pi * radius_current))
        theta_current=(2 * pi / circle_lightray_point_number) * ((arange_(1,circle_lightray_point_number)) - 1) + 2 * pi * rand_(1,1)
        x_temp=radius_current * cos_(theta_current)
        y_temp=radius_current * sin_(theta_current)
        x_lightray_coordinates=matlabarray([x_lightray_coordinates,x_temp])
        y_lightray_coordinates=matlabarray([y_lightray_coordinates,y_temp])
    x_lightray_coordinates=[x_lightray_coordinates,0].T
    y_lightray_coordinates=[y_lightray_coordinates,0].T
    return x_lightray_coordinates,y_lightray_coordinates
def load_lightfield_data_(piv_simulation_parameters=None,optical_system=None,mie_scattering_data=None,frame_index=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 4-[piv_simulation_parameters,optical_system,mie_scattering_data,frame_index].count(None)+len(args)

    object_distance=piv_simulation_parameters.lens_design.object_distance
    focal_length=piv_simulation_parameters.lens_design.focal_length
    x_camera_angle=piv_simulation_parameters.camera_design.x_camera_angle
    y_camera_angle=piv_simulation_parameters.camera_design.y_camera_angle
    data_directory=piv_simulation_parameters.particle_field.data_directory
    data_filename_prefix=piv_simulation_parameters.particle_field.data_filename_prefix
    particle_number=piv_simulation_parameters.particle_field.particle_number
    gaussian_beam_fwhm=piv_simulation_parameters.particle_field.gaussian_beam_fwhm
    perform_mie_scattering=piv_simulation_parameters.particle_field.perform_mie_scattering
    refractive_index=optical_system.design.optical_element.optical_element.element_properties.refractive_index
    front_surface_radius=optical_system.design.optical_element.optical_element.element_geometry.front_surface_radius
    back_surface_radius=optical_system.design.optical_element.optical_element.element_geometry.back_surface_radius
    optical_system_length=optical_system.design.optical_element.optical_element.element_geometry.vertex_distance
    if perform_mie_scattering:
        particle_diameter_index_distribution=mie_scattering_data.particle_diameter_index_distribution
        irradiance_constant=500 / 10000.0
    else:
        particle_diameter_index_distribution=matlabarray([])
        irradiance_constant=500
    image_distance=(1 / focal_length - 1 / object_distance) ** - 1
    h1_principal_plane=- (focal_length * (refractive_index - 1) * optical_system_length) / (back_surface_radius * refractive_index)
    h2_principal_plane=- (focal_length * (refractive_index - 1) * optical_system_length) / (front_surface_radius * refractive_index)
    v2_vertex_plane=image_distance + h2_principal_plane
    v1_vertex_plane=v2_vertex_plane + optical_system_length
    z_object=v1_vertex_plane - h1_principal_plane + object_distance
    particle_data_list=dir_([data_directory,data_filename_prefix,char('*.mat')])
    particle_data_filename_read=matlabarray([data_directory,particle_data_list[frame_index].name])
    load_(particle_data_filename_read)
    X=X_(arange_(1,particle_number))
    Y=Y_(arange_(1,particle_number))
    Z=Z_(arange_(1,particle_number))
    gaussian_sigma=gaussian_beam_fwhm / (2 * sqrt_(2 * log_(2)))
    R=irradiance_constant * (1 / (gaussian_sigma * sqrt_(2 * pi))) * exp_(- (Z ** 2) / (2 * gaussian_sigma ** 2))
    X,Y,Z=rotate_coordinates_(X,Y,Z,x_camera_angle,y_camera_angle,0,0,0,0,nargout=3)
    Z=Z + z_object
    lightfield_source.x=X
    lightfield_source.y=Y
    lightfield_source.z=Z
    lightfield_source.radiance=R
    lightfield_source.diameter_index=particle_diameter_index_distribution
    return lightfield_source
def rotate_coordinates_(X=None,Y=None,Z=None,Alpha=None,Beta=None,Gamma=None,XC=None,YC=None,ZC=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 9-[X,Y,Z,Alpha,Beta,Gamma,XC,YC,ZC].count(None)+len(args)

    R=calculate_rotation_matrix_(Alpha,Beta,Gamma)
    XR=X - XC
    YR=Y - YC
    ZR=Z - ZC
    XR=XR[:].T
    YR=YR[:].T
    ZR=ZR[:].T
    WR=R * [[XR],[YR],[ZR]]
    XR=WR[1,:]
    YR=WR[2,:]
    ZR=WR[3,:]
    XR=reshape_(XR,size_(X))
    YR=reshape_(YR,size_(Y))
    ZR=reshape_(ZR,size_(Z))
    XR=XR + XC
    YR=YR + YC
    ZR=ZR + ZC
    return XR,YR,ZR
def calculate_rotation_matrix_(theta_x=None,theta_y=None,theta_z=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 3-[theta_x,theta_y,theta_z].count(None)+len(args)

    rotation_x=matlabarray([[1,0,0],[0,cos_(theta_x),sin_(theta_x)],[0,- sin_(theta_x),cos_(theta_x)]])
    rotation_y=matlabarray([[cos_(theta_y),0,- sin_(theta_y)],[0,1,0],[sin_(theta_y),0,cos_(theta_y)]])
    rotation_z=matlabarray([[cos_(theta_z),sin_(theta_z),0],[- sin_(theta_z),cos_(theta_z),0],[0,0,1]])
    rotation_matrix=rotation_x * rotation_y * rotation_z
    return rotation_matrix
def create_camera_optical_system_(piv_simulation_parameters=None,*args,**kwargs):
    varargin = cellarray(args)
    nargin = 1-[piv_simulation_parameters].count(None)+len(args)

    focal_length=piv_simulation_parameters.lens_design.focal_length
    aperture_f_number=piv_simulation_parameters.lens_design.aperture_f_number
    optical_system=copy_(create_single_lens_optical_system)
    lens_pitch=focal_length / aperture_f_number
    lens_radius_of_curvature=100000.0
    lens_thickness=(lens_radius_of_curvature - sqrt_(lens_radius_of_curvature ** 2 - lens_pitch ** 2)) / 2
    refractive_index_1=(2 * lens_thickness * focal_length - 2 * focal_length * lens_radius_of_curvature - lens_radius_of_curvature ** 2 - lens_radius_of_curvature * sqrt_(- 4 * lens_thickness * focal_length + (2 * focal_length + lens_radius_of_curvature) ** 2)) / (2 * focal_length * (lens_thickness - 2 * lens_radius_of_curvature))
    refractive_index_2=(2 * lens_thickness * focal_length - 2 * focal_length * lens_radius_of_curvature - lens_radius_of_curvature ** 2 + lens_radius_of_curvature * sqrt_(- 4 * lens_thickness * focal_length + (2 * focal_length + lens_radius_of_curvature) ** 2)) / (2 * focal_length * (lens_thickness - 2 * lens_radius_of_curvature))
    refractive_index_temp=[isreal_(refractive_index_1),isreal_(refractive_index_2)].dot([refractive_index_1 >= 1,refractive_index_2 >= 1]).dot([refractive_index_1,refractive_index_2])
    refractive_index_temp[refractive_index_temp == 0]=Inf
    refractive_index=min_(refractive_index_temp)
    optical_system.design.optical_element(1).optical_element(1).element_geometry.front_surface_shape=[char('-sqrt(('),num2str_(lens_radius_of_curvature),char(')^2-(x.^2+y.^2))')]
    optical_system.design.optical_element(1).optical_element(1).element_geometry.back_surface_shape=[char('+sqrt(('),num2str_(lens_radius_of_curvature),char(')^2-(x.^2+y.^2))')]
    optical_system.design.optical_element(1).optical_element(1).element_geometry.pitch=lens_pitch
    optical_system.design.optical_element(1).optical_element(1).element_geometry.front_surface_radius=+ lens_radius_of_curvature
    optical_system.design.optical_element(1).optical_element(1).element_geometry.back_surface_radius=- lens_radius_of_curvature
    optical_system.design.optical_element(1).optical_element(1).element_geometry.vertex_distance=lens_thickness
    optical_system.design.optical_element(1).optical_element(1).element_properties.refractive_index=refractive_index
    optical_system.design.optical_element(1).optical_element(1).element_properties.thin_lens_focal_length=focal_length
    return optical_system
def create_single_lens_optical_system_(*args,**kwargs):
    varargin = cellarray(args)
    nargin = 0-[].count(None)+len(args)

    optical_system=copy_(struct)
    optical_system.distance_units=char('micron')
    optical_system.angle_units=char('degrees')
    optical_system.design=struct
    optical_system.design.element_type=char('system')
    optical_system.design.element_number=1
    optical_system.design.elements_coplanar=false
    optical_system.design.z_inter_element_distance=0
    optical_system.design.axial_offset_distances=[0,0]
    optical_system.design.rotation_angles=[0,0,0]
    optical_system.design.element_geometry=struct
    optical_system.design.element_geometry=[]
    optical_system.design.element_properties=struct
    optical_system.design.element_properties=[]
    optical_system.design.optical_element(1).element_type=char('system')
    optical_system.design.optical_element(1).element_number=1
    optical_system.design.optical_element(1).elements_coplanar=false
    optical_system.design.optical_element(1).z_inter_element_distance=10000.0
    optical_system.design.optical_element(1).axial_offset_distances=[0,0]
    optical_system.design.optical_element(1).rotation_angles=[0 * pi / 180,0 * pi / 180,0]
    optical_system.design.optical_element(1).element_geometry=struct
    optical_system.design.optical_element(1).element_geometry=[]
    optical_system.design.optical_element(1).element_properties=struct
    optical_system.design.optical_element(1).element_properties=[]
    optical_system.design.optical_element(1).optical_element=struct
    optical_system.design.optical_element(1).optical_element(1).element_type=char('lens')
    optical_system.design.optical_element(1).optical_element(1).element_number=[]
    optical_system.design.optical_element(1).optical_element(1).elements_coplanar=[]
    optical_system.design.optical_element(1).optical_element(1).z_inter_element_distance=0.0
    optical_system.design.optical_element(1).optical_element(1).axial_offset_distances=[0,0]
    optical_system.design.optical_element(1).optical_element(1).rotation_angles=[0,0,0]
    optical_system.design.optical_element(1).optical_element(1).element_geometry=struct
    optical_system.design.optical_element(1).optical_element(1).element_geometry.front_surface_shape=char('-sqrt((200e3)^2-(x.^2+y.^2))')
    optical_system.design.optical_element(1).optical_element(1).element_geometry.back_surface_shape=char('+sqrt((400e3)^2-(x.^2+y.^2))')
    optical_system.design.optical_element(1).optical_element(1).element_geometry.pitch=100000.0
    optical_system.design.optical_element(1).optical_element(1).element_geometry.front_surface_spherical=true
    optical_system.design.optical_element(1).optical_element(1).element_geometry.back_surface_spherical=true
    optical_system.design.optical_element(1).optical_element(1).element_geometry.front_surface_radius=+ 200000.0
    optical_system.design.optical_element(1).optical_element(1).element_geometry.back_surface_radius=- 400000.0
    optical_system.design.optical_element(1).optical_element(1).element_geometry.vertex_distance=10000.0
    optical_system.design.optical_element(1).optical_element(1).element_properties=struct
    optical_system.design.optical_element(1).optical_element(1).element_properties.refractive_index=1.5
    optical_system.design.optical_element(1).optical_element(1).element_properties.abbe_number=[]
    optical_system.design.optical_element(1).optical_element(1).element_properties.thin_lens_focal_length=85000.0
    optical_system.design.optical_element(1).optical_element(1).element_properties.transmission_ratio=1
    optical_system.design.optical_element(1).optical_element(1).element_properties.absorbance_rate=0
    return optical_system