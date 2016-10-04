# include	<stdio.h>
# include	"Test.h"

int		_K4Test1aET3int = 42;
float		_K4Test1aET4float = 42.42;

int main()
{
  printf("%d\n", _K4Test1aET3int);
  printf("%f\n", _K4Test1aET4float);

  _K4Test1aET3int = 12;
  printf("%d\n", _K4Test1aET3int);

  int i = _K4Test1fER3intA2_3int4char(2, 'a');

  printf("%c\n", (char)i);
  return (0);
}
