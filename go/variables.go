package main

import "fmt"

func main() {

    var s1 string = "hello"
    var s2 = "hello"            // infer the type of initialized variables
    s3 := "hello"               // shorthand syntax for declaring and initializing a variable

    fmt.Println(s1)
    fmt.Println(s2)
    fmt.Println(s3)

}
