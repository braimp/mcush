/* shell interpreter
 * Peng Shulin <trees_peng@163.com> 2016
 */
#ifndef _SHELL_H_
#define _SHELL_H_


#define SHELL_CMDLINE_LEN   128
#define SHELL_ARGV_LEN      20

#define STOP_AT_INVALID_ARGUMENT    {  \
        shell_write_str( "invalid arg: " ); \
        shell_write_line( opt.value ); \
        mcush_opt_usage_fprint(stdout, argv[0], opt_spec ); \
        return -1; }


typedef struct _shell_cmd {
    const char *sname;
    const char *name;
    int (*cmd)(int argc, char *argv[]);
    const char *help;
    const char *usage;
} shell_cmd_t;


typedef struct _shell_control_block_t {
    int errno;
    int argc;
    char *argv[SHELL_ARGV_LEN];
    char cmdline[SHELL_CMDLINE_LEN+1];
    char cmdline_history[SHELL_CMDLINE_LEN+1];
    int cmdline_len;
    int cmdline_cursor;
    const char *(*prompt_hook)(void);
    const shell_cmd_t *cmd_table;
} shell_control_block_t;


/* APIs */
int  shell_init( const shell_cmd_t *cmd_table );
void shell_run( void );
void shell_set_prompt_hook( const char *(*hook)(void) );
const shell_cmd_t *shell_set_cmd_table( const shell_cmd_t *cmd_table );
void shell_set_errno( int errno );
int shell_get_errno( void );
int shell_read_char( char *c );
void shell_write_char( char c );
void shell_write_str( const char *str );
void shell_write_line( const char *str );
void shell_write_int( int i );
void shell_write_float( float f );
void shell_write_hex( int x );
int shell_printf( char *fmt, ... );


/* driver APIs needed */
extern int  shell_driver_init( void );
extern void shell_driver_reset( void );
extern int  shell_driver_read( char *buffer, int len );
extern int  shell_driver_read_char( char *c );
extern int  shell_driver_read_char_blocked( char *c, int block_time );
extern int  shell_driver_read_is_empty( void );
extern int  shell_driver_write( const char *buffer, int len );
extern void shell_driver_write_char( char c );


#endif

