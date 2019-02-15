package main

import "fmt"

func main() {

    x := 18

    if x > 10 {
        fmt.Println("ok")
    } else if x >= 0 {
        fmt.Println("no")
    } else {
        fmt.Println("err")
    }

}
