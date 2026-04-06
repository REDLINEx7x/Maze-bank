*This project has been created as part of the 42 curriculum by moamhouc.*

# A-Maze-ing

## Description

A-Maze-ing is a Python-based maze generation and solving application. The project creates random mazes using a depth-first search algorithm(DFS) and solves them using breadth-first search (BFS). The application features a colorful terminal-based renderer with support for animated maze display and solution visualization.

**Goal**: Generate perfect (and imperfect) mazes and find the shortest path from entry to exit while providing an interactive, visually appealing user experience.

**Key Features**:
- Procedural maze generation with customizable dimensions
- Optional "42" pattern overlay (Easter egg for 42 School)
- Shortest path solving using BFS algorithm
- Colorful ASCII terminal rendering with animation
- Interactive menu for regeneration and visualization control
- Configuration file support for customizable maze parameters
- Solution export to text file

## Instructions

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Installation

```sh
cd Maze-bank
make install
```

### Compilation & Execution

**Run the application**:
```sh
make run
```

Or manually:
```sh
python3 a_maze_ing.py config.txt
```

**Debug mode** (with pdb):
```sh
make debug
```

**Linting & Type Checking**:
```sh
make lint          # Standard checks
make lint-strict   # Strict mypy validation
```

**Clean cache files**:
```sh
make clean
```

### Configuration File Format

The `config.txt` file controls maze parameters:

```
WIDTH=15
HEIGHT=15
ENTRY=1,0
EXIT=10,10
OUTPUT_FILE=maze.txt
PERFECT=True
```

**Configuration Keys**:
- `WIDTH` (integer): Number of columns in the maze
- `HEIGHT` (integer): Number of rows in the maze
- `ENTRY` (x,y): Starting position (column, row)
- `EXIT` (x,y): Goal position (column, row)
- `OUTPUT_FILE` (string): Output filename for maze data
- `PERFECT` (boolean): `True` for perfect maze (no loops), `False` to add extra paths
- `SEED` (optional integer): Random seed for reproducibility

**Constraints**:
- Entry and Exit must be different cells
- Entry and Exit must be within maze bounds
- Entry and Exit cannot overlap with the "42" pattern (if present)

## Maze Generation Algorithm

### Algorithm: Depth-First Search (DFS) with Recursive Backtracking

**Why DFS?**
- Guarantees a perfect maze (connected, no loops) when `PERFECT=True`
- Efficient O(n) time complexity where n = number of cells
- Creates aesthetically pleasing mazes with long, winding passages
- Simple recursive implementation
- Memory efficient for typical maze sizes

**Algorithm Steps**:
1. Initialize grid with all walls (each cell = 15 in binary)
2. Create "42" pattern if maze is large enough (optional overlay)
3. Start DFS from entry point:
   - Mark current cell as visited
   - Randomly shuffle adjacent directions
   - For each unvisited neighbor:
     - Remove walls between current and neighbor cells
     - Recursively carve from neighbor
4. If `PERFECT=False`, add extra paths via wall removal algorithm

**Wall Representation** (4-bit flags):
- Bit 0 (1): NORTH wall
- Bit 1 (2): EAST wall
- Bit 2 (4): SOUTH wall
- Bit 3 (8): WEST wall
- Value 15 (0xF): All walls present
- Value 0: All walls removed

### Solving Algorithm: Breadth-First Search (BFS)

**Why BFS?**
- Guarantees shortest path
- O(n + m) complexity where n = cells, m = edges
- Simple queue-based implementation
- Optimal for unweighted graphs

**Algorithm**:
1. Convert entry/exit coordinates from (col, row) to (row, col)
2. Initialize queue with start position and empty path
3. While queue not empty:
   - Dequeue cell and current path
   - If at exit, return path
   - For each accessible direction (no wall blocking):
     - If unvisited and in bounds, add to queue with extended path
4. Return path as sequence of directions: 'N', 'S', 'E', 'W'

## Reusable Components

### Core Modules

**[`mazegen/maze_gen.py`](mazegen/maze_gen.py)**
- `MazeGenerator` class: Standalone maze generation engine
- Reusable for any project requiring procedural maze generation
- Supports custom dimensions, entry/exit points, and perfect/imperfect modes
- Can be imported and used independently

**[`mazegen/maze_solve.py`](mazegen/maze_solve.py)**
- `solve()` function: Universal shortest-path solver
- Works with any grid representation using wall flags
- Reusable for pathfinding in other applications

**[`parsing.py`](parsing.py)**
- `parse_config()` function: Configuration file parser
- Validates all parameters and bounds checking
- Reusable for similar configuration-driven applications

**[`display.py`](display.py)**
- `MazeRenderer` class: Terminal rendering engine
- Color cycling and animation support
- Reusable for other ASCII-based visualizations
- Can display arbitrary 4-bit wall-encoded grids

**[`output.py`](output.py)**
- `generate_output()` function: Maze serialization
- Exports maze in hex format with solution
- Portable format for other applications

## Team & Project Management

### Team
- **moamhouc**: Full-stack development (architecture, generation, solving, rendering, UI)

### Individual Roles
- Algorithm selection and implementation
- Code architecture and modularization
- Testing and validation
- Documentation

### Development Evolution

**Phase 1: Core Implementation**
- Started with basic maze generation (DFS backtracking)
- Implemented BFS solver
- Created configuration parser

**Phase 2: Visualization**
- Built terminal renderer with ASCII art
- Added color support and animation
- Integrated solution path visualization

**Phase 3: Refinement**
- Added "42" pattern feature
- Implemented loop-adding algorithm for imperfect mazes
- Enhanced input validation
- Code organization into modules

**Phase 4: Polish**
- Interactive menu system
- Output file generation
- Type hints and documentation
- Linting and testing

### What Worked Well
✓ Modular architecture allows independent testing and reuse
✓ Configuration file approach provides flexibility without code changes
✓ DFS generation produces visually interesting mazes
✓ BFS ensures optimal solutions
✓ Type hints caught many errors early
✓ Separation of concerns (generation, solving, rendering)

### What Could Be Improved
- Could add multiple generation algorithms (Prim's, Kruskal's) for comparison
- Performance optimization for very large mazes (1000x1000+)
- Save/load maze state functionality
- Animated solution playback
- Web-based interface alternative to terminal
- Unit tests for edge cases
- Support for hexagonal or other grid types

### Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python 3.8+** | Primary language |
| **Type hints** | Static type checking (mypy) |
| **flake8** | Code style/quality linting |
| **mypy** | Static type analysis |
| **Make** | Build automation |
| **Git** | Version control |

### AI Usage

AI was consulted for:
- **Algorithm verification**: Confirming DFS and BFS implementations were optimal
- **Code optimization**: Identifying performance bottlenecks
- **Documentation**: Structuring comprehensive technical explanations
- **Debugging**: Troubleshooting coordinate system conversions (col,row vs row,col)

AI was NOT used for:
- Core algorithm design or implementation
- Architecture decisions
- The interactive UI/menu system

## Usage Examples

### Generate a Standard Maze
```sh
python3 a_maze_ing.py config.txt
```

### Interactive Menu Commands
```
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Cycle maze colors
4. Quit
5. Cycle 42 pattern color
```

### Customizing Mazes

Edit `config.txt`:
```
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,19
PERFECT=False
```

Then run:
```sh
python3 a_maze_ing.py config.txt
```

### Output Format

The generated `maze.txt` contains:
- Maze in hexadecimal format (each cell's wall flags)
- Entry and exit coordinates
- Solution path as sequence of directions

Example:
```
BD3D17955555553
83C3C505553953A
...
1,0
10,10
ESESEESSSESENNWNENESSEEEENWNNEESSSESSWNWSSESSSWSSEESWWSWNWWSWNNNNESEN
```

## Technical Details

### Coordinate System
- **Internal representation**: (row, col) for grid indexing
- **Configuration format**: (col, row) or (x, y) for user-friendliness
- **Conversion**: Entry/Exit coordinates are converted when needed

### Cell Encoding
Each cell is an 8-bit integer where bits 0-3 represent walls:
```
Value | Walls
------|--------
0x1   | NORTH
0x2   | EAST
0x4   | SOUTH
0x8   | WEST
0xF   | ALL (15)
0x0   | NONE
```

### Terminal Requirements
- Minimum terminal size: `(width * 4 + 1, height * 2 + 1)` characters
- UTF-8 encoding support for special characters
- Color support (ANSI escape codes)

