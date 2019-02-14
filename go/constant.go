package main

import "fmt"

func main() {

    const s1 string = "hello"
    const s2 = "hello"            // infer the type of initialized constant

    //s2 = "hi"

    fmt.Println(s1)
    fmt.Println(s2)

}
