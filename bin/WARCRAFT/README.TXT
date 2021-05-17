

            Warcraft: Orcs and Humans
                   Revision 1.2

---------------------------------------------------------------------
- WHAT THIS READ ME TEXT CONTAINS:
---------------------------------------------------------------------
1.  System Requirements
2.  Setup and Loading 
3.  Hot Keys
4.  Unit Modifications
5.  Movement
     Attack vs. Move
6.  Network Play
     Messages on the Network
     Two player Warcraft
     Selecting Units in Two-Player Custom mode
7.  Modem Play
     Modem Init Strings
8.  Troubleshooting
     Smartdrive Conflicts
     EMM386 Conflicts
     Installing to the Network
     Out of Memory with 1.16
     Problems with direct link/modem play
9.  Making Your System Run Faster
10. Command Line Options
11. Revision History
12. CHEAT CODES!!!

---------------------------------------------------------------------
- 1.  SYSTEM REQUIREMENTS
---------------------------------------------------------------------
Warcraft has a minimum requirement of DOS 5.0 or higher.  It requires
a 100% IBM PC compatible with a 386 microprocessor or better and a
VGA monitor.  Your system should have at least four megabytes of
total memory.  Warcraft will use either EMS or XMS memory and does
not require any special memory drivers other than HIMEM.SYS.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
IMPORTANT NOTE:  If you receive a message of the form: 
"Warcraft needs an additional XXX K of memory...", please 
see "Problem #1" in the TROUBLESHOOTING SECTION in order to 
increase the memory available to your system.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


---------------------------------------------------------------------
- 2.  SETUP AND LOADING
---------------------------------------------------------------------
To install Warcraft, type "INSTALL [Enter]" at the DOS prompt 
and follow the onscreen instructions.  To configure Warcraft for your 
computer, go to the WARCRAFT directory and type "SETUP [Enter]" at the 
DOS prompt.  To run the game, type "WAR [Enter]" at the DOS prompt.


---------------------------------------------------------------------
- 3.  HOTKEYS
---------------------------------------------------------------------
There are also additional functions available during game play.

F1 or Alt-H        Help
Shift F2 - F4      Save map position for immediate recall
F2 - F4            Recall saved map position
F5                 Display overview of map
F6                 Display Unit Screen (shows units in play/units destroyed)
F7                 Economy Screen (Lists total resources harvested)
F8                 Score (This is an indication of your success,
                   including your rank and current mission objectives)
F10                Options Menu

G                  Shows the building grid for structures
C                  Centers map on selected units
Ctrl-M or Alt-M    Music (toggles between ON/OFF)
Ctrl-S or Alt-S    Sound Effects (toggles between ON/OFF)
Ctrl-X or Alt-X    Exit the program
Ctrl-Esc           Disconnects the systems in two player mode
+ / - keys         Speed up or Slow down the game speed
Esc                Cancel any command just issued in any menu
Right click        Cancel any command just issued in any menu

Shift+Click on a unit             Allows grouping of up to four units
Ctrl+Drag Mouse over units        Allows grouping of up to four units


---------------------------------------------------------------------
- 4.  UNIT MODIFICATIONS
---------------------------------------------------------------------
Both Catapults and Summoned Creatures operate in manners dissimilar
from other units in the game:

The catapult will attack enemy units automatically ONLY if there 
are no friendly units that will be effected by splash damage from the 
missile.  If you select the Attack command and specify a target, the 
catapult will fire at the selected target regardless of friendly unit 
proximity.

Summoned Creatures have a Magic Point (MP) bar as well as a
Hit Point (HP) bar. The MP bar will degrade over time, and when it is 
drained, the summoned creature will begin taking damage, as the powers 
that hold it here are no longer in force.


---------------------------------------------------------------------
- 5.  MOVEMENT
---------------------------------------------------------------------
ATTACK VS. MOVE
When a Unit is instructed to Move, it will head to the selected location and 
ignore anything that crosses it path, including units that attack it. This 
allows for uninterrupted movement, as well as enforced retreats.

When a Unit is instructed to Attack, you may choose either an area to attack, 
or a specific target.

When you choose an area to Attack, the unit will move there, but if he is 
attacked in transit, the unit will stop and respond to the attack.  When the 
unit arrives at the selected location, it will look for immediate targets 
within its range to attack.

When you choose a specific target to Attack, your unit will move to engage 
the selected target, ignoring all other enemies or threats.


---------------------------------------------------------------------
- 6.  NETWORK PLAY
---------------------------------------------------------------------
IMPORTANT NOTE:  Warcraft requires the IPX network protocol.


NODE NUMBERS
The node number option in network play allows two players to find each other
when more than one game of Warcraft is starting on the network.  Choose the
same node number for both players.


MESSAGES ON THE NETWORK
Messages can be sent to an opposing player in a Two-Player game by simply 
pressing the Enter key. A MSG: prompt will appear at the bottom of the screen.  
Type in your message, and then press Enter to send it.

SELECTING UNITS IN TWO-PLAYER CUSTOM MODE
In a Two-Player Custom game, players can either have the default setting
of two Peons/Peasants or they can elect to create custom armies through 
the Select Armies dialog.  Not only can you affect what units you are 
choosing for your side, but you may select or deselect units for the 
enemy side by using the mouse to click the arrow keys in the Unit Selection 
area.  If you wish to negate the ability to create specific units, they 
may be turned OFF in the same manner, making them unavailable for play.

SELECTING UNITS IN ONE-PLAYER CUSTOM MODE
In one player custom mode, you may choose to change the number of
units you start with in your fight against the computer player.  The
computer player's units are fixed and cannot be altered.


---------------------------------------------------------------------
- 7.  MODEM PLAY
---------------------------------------------------------------------
For best performance you will want to disable compression and error control 
on your modem.  Here are some init strings for popular modems that we have 
found to work well.

HAYES ACCURA 144B, ZOOM 14400, PRACTICAL PERIPHERALS, MOST HAYES COMPATIBLES:
    AT &K0 M1 S46=0 &D2 &Q6

US ROBOTICS SPORTSTER:
    CLEAR string set to:AT &F0
    AT &K0 M1 &M0 &D2

INTEL 14.4:
    AT &F\N0\Q0

2400 BAUD MODEMS:
    CLEAR and INIT strings set to ATZ

If your system does not run smoothly during MODEM or DIRECT LINK
play, these are some suggestions which may help:

    * You can turn music OFF to increase game speed

    * Decreasing the BAUD rate may increase game speed


---------------------------------------------------------------------
- 8.  TROUBLESHOOTING
---------------------------------------------------------------------
Most systems should experience no difficulties running Warcraft.  
However, a small percentage of systems may experience occasional
system conflicts.  Many of these problems are quite easy to fix
using the information provided below.  Before attempting to
remedy any problem, we urge you to save your important system 
files (AUTOEXEC.BAT and CONFIG.SYS in particular) before making
any modifications.  Please refer to your system's documentation
before making any changes.

--------------
Problem #1:
    I don't have enough free memory to play Warcraft
--------------
Here are several solutions to increase your free memory:

   * Remove unneeded TSR programs from memory

   * Remove SMARTDRIVE, or reduce the size of its disk cache
    to do this, edit the smartdrive line in your autoexec.bat file
    to a lower number, i.e., change C:\dos\smartdrv.exe 1024 256 /x
    to C:\dos\smartdrv 256 /x.  The first number is the cache size.

   * Run the memory optimizer that comes with your memory manager
     (MemMaker for EMM386, Maximize for 386MAX, Optimize with QEMM, etc)

--------------
Problem #2:
    The install program cannot install the program
    to my hard disk due to an error condition.
--------------
A SMARTDRIVE conflict is the most likely cause of this problem.  
see the solution to Problem #1 above.

If you are using NDOS from SYMANTEC/Norton Utilites, the installer
may be unable to copy Warcraft onto your hard disk.  Remove NDOS
and try to install again.


--------------
Problem #3:
    Warcraft occasionally "freezes" or displays irregular behavior.
--------------
EMM386.EXE is the most likely cause of irregular behavior.  There are
several known problems with EMM386.EXE which prevent proper program
operation.  We recommend trying the following alternatives:
(this list courtesy of Rational Systems Extenders)

    * Run with HIMEM.SYS only (This will also speed 
      your system performance).

    * Replace EMM386 with another memory manager, such 
      as QEMM-386 or 386Max.

    * Run in a Windows DOS box.

    * Configure EMM386 with both the NOEMS and NOVCPI options.

    * Convert the DEVICEHIGH statements in your CONFIG.SYS to 
      DEVICE statements, and remove the LH (Load High) commands
      from your AUTOEXEC.BAT.

Also, if you have an older version mouse driver, try updating to
a more recent version.

--------------
Problem #4:
    Warcraft does not work properly when I run it from a network drive.
--------------
Warcraft should run properly using most network cards.  A few network
cards may cause sporadic crashes while running Warcraft.  Try
playing Warcraft from the CD (MINIMAL install), or perform a PARTIAL
or FULL install to your local hard disk.


--------------
Problem #5:
    I have two monitors, and Warcraft runs very slowly on my system.
--------------
If you are using a monochrome monitor in addition to your VGA color monitor,
the Diamond Stealth video card will cause the game to run very slowly.
Other video cards may also display similar problems.  Removing the 
monochrome card is highly recommended.  


--------------
Problem #6:
    The SAVE/LOAD game feature doesn't work properly,
    or causes my system to "freeze" occasionally.
--------------

If you have SMARTDRIVE installed with WRITE-CACHING, the SAVE/LOAD 
feature may not work properly.  This is due to problems with
SMARTDRIVE and DOS. Every version of SMARTDRIVE we have tested
from v4.0 through v5.01 has write-caching conflicts.  Either disable 
write-caching on the hard disk containing WAR.EXE or remove SMARTDRIVE
altogether.

Example:  if WAR.EXE is installed on the C: drive, try using the
following command to remove write-caching:

    SMARTDRV C


--------------
Problem #7:
    I upgraded to a new version of Warcraft,
    and now I'm getting out of memory errors.
--------------
    The new version of Warcraft takes about another 20k memory to
    run....see the solution to problem #1 above.


--------------
Problem #8:
    I can't get my modem/direct link game to work correctly
--------------
    run Warcraft with the dlink option enabled, for example,

    WAR DLINK

    Also, if you have a modem on com 4, and are attempting a 
    direct link game on com 2, or vice versa, the modem may
    interfere with the direct link.  Try setting the modem to 
    a different com port, or connecting on a different one.
    The same is true for the pair of com 1 and com 3.

--------------
Problem #9:
    I have a Wave Jammer sound card, but the setup program 
    doesn't find it.
--------------
    The Wave Jammer driver requires that you have defined
    a BLASTER environment variable.  To do this, add the 
    following line to your autoexec.bat file:

	    set BLASTER=a220 i5 d1 t4


---------------------------------------------------------------------
- 9.  MAKING YOUR SYSTEM RUN FASTER
---------------------------------------------------------------------
Adjust the speed using the Options Dialog or the + or - keys.

The EMM 386 memory manager (EMM386.EXE) slows the game speed of Warcraft
considerably.  Use HIMEM.SYS only (without EMM386), or another memory 
manager like QEMM or 386MAX to increase game speed.  Refer to your 
DOS manual to change your memory configuration.  Also, please refer to 
the notes regarding EMM386.EXE in the TROUBLESHOOTING section.


---------------------------------------------------------------------
- 10.  COMMAND LINE OPTIONS
---------------------------------------------------------------------
Warcraft has two command line options:

war file=<filename> where <filename> equals an alternate config. file  
            The default is config.war

war dlink enables the enhanced communication routines

war ? lists these options


---------------------------------------------------------------------
- 11.  REVISION HISTORY
---------------------------------------------------------------------
1.21:
    Fixed digital sound support for certain sound cards.

1.20:
    Significantly improved speed for slower systems
    Corrected irregular slow modem play for all modems
	Added support for WaveJammer and RAP 10 sound cards
	Updated Pro Audio sound drivers
	Added WAR_EDIT.EXE utility for extra FUN!

1.16:
    Added command line option for enhanced connectivity 
    Final copy protection enhancement

1.15:
    Enhanced direct link and modem connectivity
    Fixed bug affecting scores over 12,000
    Improved copy protection for ease of use
    Gravis UltraSound support added

1.14:
    Fixed speech bug

1.13:
    Replaced CD-ROM copy protection with floppy copy protection
    Fixed human level 7 bug
    Updated DOS 4/GW extender

			    
---------------------------------------------------------------------
- 12.  CHEAT CODES!!!
---------------------------------------------------------------------
To enable a cheat, first start a game by choosing either "New Game"
or "Load Game".  Once the game has started, press the return key.
Near the botton of the screen, you will see the string "MSG: ".
Type any of the codes below and press return.  If the cheat was typed
correctly, you will see the message:
    "CHEAT ENABLED YOU WASCALLY WABBIT!"

If you type the same cheat code again, the cheat will be disabled
(where appropriate).  Please note that in a Two-Player game, these 
codes will affect both sides.

Warcraft has a Master Code that is required to enable the cheat codes 
listed below, and it must be entered before any of the codes will work.


MASTER CODE: CORWIN OF AMBER

CODE                    EFFECT
------------------------------
HUMAN1    ORC1          goto to human level 1 or orc level 1
HUMAN2    ORC2          ditto for level 2
...       ...           etc.
HUMAN12   ORC12         ditto for level 12
                        This cheat works only in one player mode

YOURS TRULY             Takes player to the victory sequence
                        This cheat works only in Campaign Mode

CRUSHING DEFEAT         Takes player to the loss sequence
                        This cheat works only in Campaign Mode

IDES OF MARCH           Takes player to the finale sequence

POT OF GOLD             Adds 10,000 gold and 5,000 lumber to your reserves

EYE OF NEWT             Upgrades your magic users with all spells

IRON FORGE              Upgrades all technologies immediately

SALLY SHEARS            Displays the entire map area

HURRY UP GUYS           All buildings, units and upgrades are built/trained 
                        at an accelerated rate

THERE CAN BE ONLY ONE   All of your units are invulnerable except by a 
                        direct catapult hit, and will inflict 255 points 
                        of damage per hit.


