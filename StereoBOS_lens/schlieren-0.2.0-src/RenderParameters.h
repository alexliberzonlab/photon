#ifndef RENDERPARAMETERS_H
#define RENDERPARAMETERS_H

//#include "cutil.h"
//#include "cutil_math.h"
//#include <cuda.h>
////#include "cuda_gl_interop.h"
//#include <cstdlib>
//#include <float.h>
#include <vector_types.h>
#include <string>
#include <sstream>

using namespace std;
enum cutoffs {CUTOFF_NONE = 0, CUTOFF_KNIFE_X, CUTOFF_KNIFE_NEGATIVE_X,
              CUTOFF_KNIFE_Y = 3, CUTOFF_KNIFE_NEGATIVE_Y, CUTOFF_PINHOLE, CUTOFF_INVERSE_PINHOLE,
              CUTOFF_INTERFOREMETRY, CUTOFF_IMAGE, CUTOFF_TRACE};
struct LightField
{
  float3* pos;
  float3* dir;
};

 struct RenderParameters
{
    unsigned int data_width, data_height, data_depth;
    float data_min;
    float4* data;
    //float4* color_data;  //used for color accululation of volume
    float* data2;
    float4* inout_rgb;  //color information on film plane
    unsigned int* out_rgb; //filtered output texture
    unsigned int* source_rgb; //BOS pattern
    unsigned int width, height;  // image height and width (pixels)
    float3 min_bound, max_bound;
  
    string inputFilename;
    // Camera Parameters
    float3 camera_corner, camera_pos, camera_x, camera_y, camera_z;
    float r; // radius of curvature
	float t; // thickness 
	float n; // refractive index

    float R; // Distance of camera center from origin of world co-ord
    float _rot_x, _rot_y, _rot_z; // Orientation of camera axes with respect to the world co-ordinate axes (Radians)
    float c;	          // Principal Distance - distance of pinhole from center of camera plane
    float pitch, pitch_random;		      // Pitch or Aperture of the pinhole

    float3 pos_c; // Position of BOS Target in world co-ord 
    float stepSize, projectionDistance;

    float* random_array_theta; float* random_array_phi; int random_array_size;
    float* random_array;
    float rand1, rand2, rand3, rand4;
    unsigned int raysPerPixel, numRenderPasses;
    float dataScalar;
    float cutoffScalar;
    int num_zero, raysPerPoint;
    //LightField* lightfieldp;
    bool threadSafe, useOctree, useRefraction;
    int cutoff;
    bool cutoff_dirty;  //needs to be re-uploaded to card

    float4* cutoff_rgb;  //image of filter
    uint2 cutoffSize;
    unsigned int passes;
};



#endif // RENDERPARAMETERS_H
