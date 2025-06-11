"""
Configuration settings for the Wrong Material Detector application.
"""
import os

# Debug mode flag
DEBUG = False

# Base paths
BASE_CSV_PATH = r'\\192.168.2.10\csv\csv'
SOUND_PATH = r'\\192.168.2.19\ai_team\AI Program\Programs\Individual Program\Sounds'

# Serial configuration
SERIAL_PORT = 'COM7'  # Default COM port for PLC communication
SERIAL_BAUD = 9600   # Default baud rate for PLC communication

# Process configurations
PROCESS_CONFIGS = {
    1: {
        'csv_path': os.path.join(BASE_CSV_PATH, 'VT1', 'Debug' if DEBUG else ''),
        'model_codes': ['60CAT0213P', '60CAT0212P', '60CAT0202P', '60CAT0203P', 
                     '60CAT0902P', '60CAT0903P', '60CAT0905P', '60CAT0000P'],
        'material_checks': {
            'Em2p': 'Process 1 Em2p',  # EM0580106P
            'Em3p': 'Process 1 Em3p',  # EM0580107P
            'Harness': 'Process 1 Harness',  # RC03221254-03A
            'Frame': 'Process 1 Frame',  # FM05000102-01A/00A
            'Bushing': 'Process 1 Bushing'  # CG00300500-02A
        }
    },
    2: {
        'csv_path': os.path.join(BASE_CSV_PATH, 'VT2', 'Debug' if DEBUG else ''),
        'model_codes': ['60CAT0213P', '60CAT0212P', '60CAT0202P', '60CAT0203P',
                     '60CAT0902P', '60CAT0903P', '60CAT0905P', '60CAT0000P'],
        'material_checks': {
            'M4x40 Screw': 'Process 2 M4x40 Screw',  # NE044014A0-B/NE044021A0
            'Rod Blk': 'Process 2 Rod Blk',  # RDB5200200/FM03500100-01
            'Df Blk': 'Process 2 Df Blk',  # DFB6600600/DFB6600610
            'Df Ring': 'Process 2 Df Ring',  # DR06400400-01A
            'Washer': 'Process 2 Washer',  # WA04090110-B
            'Lock Nut': 'Process 2 Lock Nut'  # NT04090340-B/RDB4200801-01A
        }
    },
    3: {
        'csv_path': os.path.join(BASE_CSV_PATH, 'VT3', 'Debug' if DEBUG else ''),
        'model_codes': ['60CAT0213P', '60CAT0212P', '60CAT0202P', '60CAT0203P',
                     '60CAT0902P', '60CAT0903P', '60CAT0905P', '60CAT0000P'],
        'material_checks': {
            'Frame Gasket': 'Process 3 Frame Gasket',  # PK01501131-01/PK01501133-00
            'Casing Blk': 'Process 3 Casing Block',  # CSB6400802
            'Casing Gasket': 'Process 3 Casing Gasket',  # PK01501140-00/PK01501143-00
            'M4x16 Screw 1': 'Process 3 M4x16 Screw 1',  # NE041614A0-B
            'M4x16 Screw 2': 'Process 3 M4x16 Screw 2',  # NE041617A7-B
            'Ball Cushion': 'Process 3 Ball Cushion',  # DK01400104-00/DK01400102-01
            'Frm Cover': 'Process 3 Frame Cover',  # NI08170103-03
            'Partition Board': 'Process 3 Partition Board',  # LK13000100-01A
            'Tube 1': 'Process 3 Built In Tube 1',  # LK00900200-00
            'Tube 2': 'Process 3 Built In Tube 2', # BC08000300-02A
            'Head Cover': 'Process 3 Head Cover', # HC08000100-00
            'Casing Packing': 'Process 3 Casing Packing', # CP08000100-00
            'M4x12 Screw': 'Process 3 M4x12 Screw', # NE041214A0-B
            'Csb L': 'Process 3 Csb L', # CSB6400801
            'Csb R': 'Process 3 Csb R', # CSB6400802
            'Head Packing': 'Process 3 Head Packing' # HP08000100-00
        }
    },
    4: {
        'csv_path': os.path.join(BASE_CSV_PATH, 'VT4', 'Debug' if DEBUG else ''),
        'model_codes': ['60CAT0213P', '60CAT0212P', '60CAT0202P', '60CAT0203P',
                     '60CAT0902P', '60CAT0903P', '60CAT0905P', '60CAT0000P'],
        'material_checks': {
            'Tank': 'Process 4 Tank',  # TK08000603-09/TKB8000602
            'Upper Housing': 'Process 4 Upper Housing',  # PK01501142-02/PK01501141-01
            'Cord Hook': 'Process 4 Cord Hook',  # PK01501132-01/NI08170102-00
            'M4x16 Screw': 'Process 4 M4x16 Screw',  # NE041201A0
            'Tank Gasket': 'Process 4 Tank Gasket',  # NE04402130/NE044021A0
            'Tank Cover': 'Process 4 Tank Cover',  # HU06020011-03A/HU06020001-01
            'Housing Gasket': 'Process 4 Housing Gasket',  # NE041614A0-B
            'M4x40 Screw': 'Process 4 M4x40 Screw', # NE044014A0-B
            'Partition Gasket': 'Process 4 PartitionGasket', # PG08000100-00
            'M4x12 Screw': 'Process 4 M4x12 Screw', # NE041214A0-B
            'Muffler': 'Process 4 Muffler', # MU08000100-00
            'Muffler Gasket': 'Process 4 Muffler Gasket', # MG08000100-00
            'VCR': 'Process 4 VCR'
        }
    },
    5: {
        'csv_path': os.path.join(BASE_CSV_PATH, 'VT5', 'Debug' if DEBUG else ''),
        'model_codes': ['60CAT0213P', '60CAT0212P', '60CAT0202P', '60CAT0203P',
                     '60CAT0902P', '60CAT0903P', '60CAT0905P', '60CAT0000P'],
        'material_checks': {
            'Rating Label': 'Process 5 Rating Label'  # BC06070400-00
        }
    },
    6: {
        'csv_path': os.path.join(BASE_CSV_PATH, 'VT6', 'Debug' if DEBUG else ''),
        'model_codes': ['60CAT0213P', '60CAT0212P', '60CAT0202P', '60CAT0203P',
                     '60CAT0902P', '60CAT0903P', '60CAT0905P', '60CAT0000P'],
        'material_checks': {
            'Vinyl': 'Process 6 Vinyl' # NE041205A0
        }
    }
}

# Sound configurations
SOUND_TITLES = {
    # Process 1 sounds
    'Process1WrongEm2P': 'Process1WrongEm2P.mp3',
    'Process1WrongEm3P': 'Process1WrongEm3P.mp3',
    'Process1WrongHarness': 'Process1WrongHarness.mp3',
    'Process1WrongFrame': 'Process1WrongFrame.mp3',
    'Process1WrongBushing': 'Process1WrongBushing.mp3',
    
    # Process 2 sounds
    'Process2WrongM4X40Screw': 'Process2WrongM4X40Screw.mp3',
    'Process2WrongRodBlock': 'Process2WrongRodBlock.mp3',
    'Process2WrongDiaphragmBlock': 'Process2WrongDiaphragmBlock.mp3',
    'Process2WrongDfRing': 'Process2WrongDfRing.mp3',
    'Process2WrongWasher': 'Process2WrongWasher.mp3',
    'Process2WrongLockNut': 'Process2WrongLockNut.mp3',
    'Process2WrongFrame': 'Process2WrongFrame.mp3',
    
    # Process 3 sounds
    'Process3WrongFrameGasket': 'Process3WrongFrameGasket.mp3',
    'Process3WrongCSB': 'Process3WrongCSB.mp3',
    'Process3WrongCasingGasket': 'Process3WrongCasingGasket.mp3',
    'Process3WrongM4X16Screw': 'Process3WrongM4X16Screw.mp3',
    'Process3WrongBallCushion': 'Process3WrongBallCushion.mp3',
    'Process3WrongFrameCover': 'Process3WrongFrameCover.mp3',
    'Process3WrongPartitionBoard': 'Process3WrongPartitionBoard.mp3',
    'Process3WrongBuiltInTube': 'Process3WrongBuiltInTube.mp3',
    'Process3WrongHeadCover': 'Process3WrongHeadCover.mp3',
    'Process3WrongCasingPacking': 'Process3WrongCasingPacking.mp3',
    'Process3WrongM4X12Screw': 'Process3WrongM4X12Screw.mp3',
    'Process3WrongCasingLeft': 'Process3WrongCasingLeft.mp3',
    'Process3WrongCasingRight': 'Process3WrongCasingRight.mp3',
    'Process3WrongHeadPacking': 'Process3WrongHeadPacking.mp3',
    
    # Process 4 sounds
    'Process4WrongTank': 'Process4WrongTank.mp3',
    'Process4WrongUpperHousing': 'Process4WrongUpperHousing.mp3',
    'Process4WrongCordHook': 'Process4WrongCordHook.mp3',
    'Process4WrongM4X16Screw': 'Process4WrongM4X16Screw.mp3',
    'Process4WrongTankGasket': 'Process4WrongTankGasket.mp3',
    'Process4WrongTankCover': 'Process4WrongTankCover.mp3',
    'Process4WrongHousingGasket': 'Process4WrongHousingGasket.mp3',
    'Process4WrongM4X40Screw': 'Process4WrongM4X40Screw.mp3',
    'Process4WrongPartitionGasket': 'Process4WrongPartitionGasket.mp3',
    'Process4WrongM4X12Screw': 'Process4WrongM4X12Screw.mp3',
    'Process4WrongMuffler': 'Process4WrongMuffler.mp3',
    'Process4WrongMufflerGasket': 'Process4WrongMufflerGasket.mp3',
    'Process4WrongFrameCover': 'Process4WrongFrameCover.mp3',
    'Process4WrongRubberLeg': 'Process4WrongRubberLeg.mp3',
    
    # Process 5 sounds
    'Process5WrongRatingLabel': 'Process5WrongRatingLabel.mp3',
    
    # Process 6 sounds
    'Process6WrongVinyl': 'Process6WrongVinyl.mp3'
}

# UI configurations
UI_CONFIG = {
    'window_title': 'Wrong Material Detector',
    'window_size': '1480x500+50+50',
    'window_position': '+50+50',
    'font_normal': ('Arial', 12),
    'font_bold': ('Arial', 12, 'bold')
} 