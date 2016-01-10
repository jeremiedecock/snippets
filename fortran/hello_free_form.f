! Usage: gfortran -ffree-form -o hello hello_free_form.f

! The Fortran 77 syntax requires 6 spaces before any commands!
! This 6 spaces rule can be turned off, by specifying the "free form"
! mode to the compiler: "gfortran -ffree-form ..."
! (source: https://en.wikibooks.org/wiki/Fortran/Beginning_Fortran)

program hello
    print *, 'Hello, world! (free form)'
end program hello

