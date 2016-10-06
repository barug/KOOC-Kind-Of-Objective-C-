#include "Test.h"

char _K4Test1aET4char = 'K';
int             _K4Test1aET3int = 42;
float           _K4Test1aET4float = 42.42;

int	_K4Test1fER3intA2_3int4char(int i, char c)
{
  return (c + i);
}

char	_K4Test1fER4charA2_3int4char(int i, char c)
{
  return (c - i);
}

void	_K4Test1fER4voidA2_3intP4char(int* i, char c)
{
  *i += c;
}
