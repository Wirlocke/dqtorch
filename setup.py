import os
import sys
from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension


# Early check for CUDA availability
try:
    import torch
    if not torch.cuda.is_available():
        print("CUDA is not available. This package requires CUDA.")
        sys.exit(1)
except ImportError:
    print("PyTorch is not installed. Please install it first.")
    sys.exit(1)

# Get the CUDA architecture for the current GPU


def get_cuda_arch():
    try:
        import torch
        major, minor = torch.cuda.get_device_capability()
        return f'{major}.{minor}'
    except:
        return None


cuda_arch = get_cuda_arch()
if cuda_arch:
    os.environ["TORCH_CUDA_ARCH_LIST"] = cuda_arch

# Define compilation flags
extra_compile_args = {
    'cxx': ['-O3', '-std=c++17'] if os.name == "posix" else ['/O2', '/std:c++17'],
    'nvcc': [
        '-O3',
        '-std=c++17',
        '-U__CUDA_NO_HALF_OPERATORS__',
        '-U__CUDA_NO_HALF_CONVERSIONS__',
        '-U__CUDA_NO_HALF2_OPERATORS__',
    ]
}

# Define the extension
ext_modules = [
    CUDAExtension(
        name='dqtorch._quaternion_cuda',
        sources=[
            'dqtorch/src/quaternion.cu',
            'dqtorch/src/bindings.cpp',
        ],
        extra_compile_args=extra_compile_args,
    )
]

setup(
    name='dqtorch',
    version='0.1.0',
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={
        'build_ext': BuildExtension,
    },
    package_data={
        'dqtorch': ['src/*.cpp', 'src/*.cu', 'src/*.h'],
    },
    zip_safe=False,
)
