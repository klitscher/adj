import adj
import collections
import ctypes
import enum
import os.path


UNICODE  = 0x80000000


@enum.unique
class Errors (enum.IntEnum):
    """Enumeration of error codes documented by the Bass library."""
    OK       = 0
    MEM      = 1
    FILEOPEN = 2
    DRIVER   = 3
    BUFLOST  = 4
    HANDLE   = 5
    FORMAT   = 6
    POSITION = 7
    INIT     = 8
    START    = 9
    SSL      = 10
    ALREADY  = 14
    NOCHAN   = 18
    ILLTYPE  = 19
    ILLPARAM = 20
    NO3D     = 21
    NOEAX    = 22
    DEVICE   = 23
    NOPLAY   = 24
    FREQ     = 25
    NOTFILE  = 27
    NOHW     = 29
    EMPTY    = 31
    NONET    = 32
    CREATE   = 33
    NO_FX    = 34
    NOTAVAIL = 37
    DECODE   = 38
    DX       = 39
    TIMEOUT  = 40
    FILEFORM = 41
    SPEAKER  = 42
    VERSION  = 43
    CODEC    = 44
    ENDED    = 45
    BUSY     = 46
    UNKNOWN  = -1

Errors.init = collections.defaultdict(lambda: (Exception, 'unknown'), {
    Errors.DX: (OSError, 'no Bass-compatible audio driver installed'),
    Errors.DEVICE: (ValueError, 'invalid sound card index number'),
    Errors.ALREADY: (TypeError, 'Bass is already initialized'),
    Errors.DRIVER: (OSError, 'no available driver'),
    Errors.BUSY: (OSError, 'something else has control of the sound card'),
    Errors.FORMAT: (OSError, 'specified frequency not supported'),
    Errors.MEM: (MemoryError, 'out of memory initializing Bass')
})

Errors.openFile = collections.defaultdict(lambda: (Exception, 'unknown'), {
    Errors.INIT: (TypeError, 'Bass has not been initialized'),
    Errors.FILEOPEN: (OSError, 'could not open music file'),
    Errors.FILEFORM: (ValueError, 'music file format not recognized'),
    Errors.CODEC: (TypeError, 'no codec installed for music file'),
    Errors.FORMAT: (TypeError, 'unsupported sample format in music file'),
    Errors.MEM: (MemoryError, 'out of memory opening music file'),
})


@enum.unique
class PositionFlags (enum.IntEnum):
    """Flags used to determine how to set the position of a channel."""
    BYTE        = 0X00000000
    MUSIC_ORDER = 0X00000001
    OGG         = 0X00000003
    DECODETO    = 0x20000000
    INEXACT     = 0x08000000
    RELATIVE    = 0x04000000
    RESET       = 0x02000000
    SCAN        = 0x40000000


@enum.unique
class SampleFlags (enum.IntEnum):
    """Flags for configuring samples playing on a channel."""
    BITS8     = 0X00001
    MONO      = 0X00002
    LOOP      = 0X00004
    D3        = 0X00008
    SOFTWARE  = 0X00010
    MUTEMAX   = 0X00020
    VAM       = 0X00040
    FX        = 0X00080
    FLOAT     = 0X00100
    OVER_VOL  = 0X10000
    OVER_POS  = 0X20000
    OVER_DIST = 0X30000


@enum.unique
class StreamFlags (enum.IntEnum):
    """Flags for configuring sample streams."""
    PRESCAN  = 0X00020000
    AUTOFREE = 0X00040000
    RESTRATE = 0X00080000
    BLOCK    = 0X00100000
    DECODE   = 0X00200000
    STATUS   = 0X00800000


@enum.unique
class SyncFlags (enum.IntEnum):
    """Flags for setting up a callback on an audio channel."""
    POS        = 0X00000000
    MUSICINST  = 0X00000001
    END        = 0X00000002
    MUSICFX    = 0X00000003
    META       = 0X00000004
    SLIDE      = 0X00000005
    STALL      = 0X00000006
    DOWNLOAD   = 0X00000007
    FREE       = 0X00000008
    MUSICPOS   = 0X0000000A
    SETPOS     = 0X0000000B
    OGG_CHANGE = 0X0000000C
    DEV_FAIL   = 0X0000000E
    DEV_FORMAT = 0X0000000F
    MIXTIME    = 0x40000000
    ONETIME    = 0x80000000


SyncCallback = ctypes.CFUNCTYPE(
    None,
    ctypes.c_uint32,
    ctypes.c_uint32,
    ctypes.c_uint32,
    ctypes.c_void_p
)


class WinGuid (ctypes.Structure):
    """Windows's low-level structure representing a GUID."""
    _fields_ = (
        ('Data1', ctypes.c_uint32),
        ('Data2', ctypes.c_ushort),
        ('Data3', ctypes.c_ushort),
        ('Data4', ctypes.c_ubyte * 8)
    )


def loadLib() -> ctypes.CDLL:
    """Load the Bass library and fill in its types with Python."""
    if adj.platform.os == 'cygwin':
        bass = ctypes.CDLL(os.path.join(adj.path, 'bass.dll'))
    elif adj.platform.os == 'mac':
        bass = ctypes.CDLL(os.path.join(adj.path, 'libbass.dynlib'))
    elif adj.platform.os == 'windows':
        bass = ctypes.WinDLL(os.path.join(adj.path, 'bass.dll'))
    else:
        bass = ctypes.CDLL(os.path.join(adj.path, 'libbass.so'))
    bass.BASS_ChannelBytes2Seconds.restype = ctypes.c_double
    bass.BASS_ChannelBytes2Seconds.argtypes = (
        ctypes.c_uint32,
        ctypes.c_uint64
    )
    bass.BASS_ChannelPause.restype = ctypes.c_bool
    bass.BASS_ChannelPause.argtypes = (ctypes.c_uint32,)
    bass.BASS_ChannelPlay.restype = ctypes.c_bool
    bass.BASS_ChannelPlay.argtypes = (ctypes.c_uint32, ctypes.c_bool)
    bass.BASS_ChannelSetPosition.restype = ctypes.c_bool
    bass.BASS_ChannelSetPosition.argtypes = (
        ctypes.c_uint32,
        ctypes.c_uint64,
        ctypes.c_uint32
    )
    bass.BASS_ChannelSeconds2Bytes.restype = ctypes.c_uint64
    bass.BASS_ChannelSeconds2Bytes.argtypes = (
        ctypes.c_uint32,
        ctypes.c_double
    )
    bass.BASS_ChannelSetSync.restype = ctypes.c_uint32
    bass.BASS_ChannelSetSync.argtypes = (
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_uint64,
        SyncCallback,
        ctypes.c_void_p
    )
    bass.BASS_ChannelStop.restype = ctypes.c_bool
    bass.BASS_ChannelStop.argtypes = (ctypes.c_uint32,)
    bass.BASS_ErrorGetCode.restype = ctypes.c_int
    bass.BASS_ErrorGetCode.argtypes = ()
    bass.BASS_Init.restype = ctypes.c_bool
    bass.BASS_Init.argtypes = (
        ctypes.c_int,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.POINTER(WinGuid)
    )
    bass.BASS_StreamCreateFile.restype = ctypes.c_uint32
    bass.BASS_StreamCreateFile.argtypes = (
        ctypes.c_bool,
        ctypes.c_void_p,
        ctypes.c_uint64,
        ctypes.c_uint64,
        ctypes.c_uint32
    )
    bass.BASS_StreamFree.restype = ctypes.c_bool
    bass.BASS_StreamFree.argtypes = (ctypes.c_uint32,)
    return bass
