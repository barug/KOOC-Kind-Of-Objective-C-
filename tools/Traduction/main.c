#include "Test.h"

int main()
{
  printf("%d\n", K4Test1aET3int);	// Need more precision from *.kc ?
  printf("%f\n", K4Test1aET3int);	// Need more precision from *.kc ?
  printf("%f\n", K4Test1aET4float);

  _K4Test1aET3int = 12;

  printf("%d\n", [Test.a]);
  printf("%d\n", _K4Test1aET3int);

  int i = _K4Test1fER3intA2_3int4char(2, 'a');

  printf("%c\n", char(i));
}
