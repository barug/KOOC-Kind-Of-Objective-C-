itf_Test	_inst_vtable_Test = {
  &²Test²clean,
  &²Test²pouet,
};

itf_Test2	_inst_vtable_Test2 = {
  &²Test2²clean,
  &²Test²pouet,
  &²Test²boum,
};

///init Test
{
  self->_vt = &_inst_vtable_Test;
}

///init Test2
{
  self->_vt = &_inst_vtable_Test2;
}

//call
{
  [moninst pouet :p1 ];
  moninst->_vt->²Test²pouet(moninst, p1);
}

void		_K4Test19myNonMemberFunctionER4voidA0_()
{}

void		_K4Test11mb_functionER4voidA0_(Test *)
{}

void		_K4Test21myOtherMemberFunctionER4voidA0_(Test *)
{}

void		_K4Test22myOtherMemberFunction2ER4voidA1_P4Test(Test *)
{}
