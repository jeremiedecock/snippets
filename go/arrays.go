package main

import "fmt"

func main() {

    var a1 [3]int

    fmt.Println(a1)

    a1[0] = 100
    fmt.Println("set:", a1)
    fmt.Println("get:", a1[0])
    fmt.Println("len:", len(a1))

    a2  := [3]int{1, 2, 3}

    fmt.Println(a2)

    a3  := []int{1, 2, 3, 4, 5, 6}

    fmt.Println(a3)
    fmt.Println(a3[2:4])
    fmt.Println(a3[:4])
    fmt.Println(a3[2:])

    a4  := [2][3]int{{1, 2, 3}, {1, 2, 3}}

    fmt.Println(a4)

}

