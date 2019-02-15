package main

import "fmt"

func main() {

    a1 := make([]int, 3)

    fmt.Println(a1)

    a1[0] = 100
    fmt.Println("set:", a1)
    fmt.Println("get:", a1[0])
    fmt.Println("len:", len(a1))

    a1 = append(a1, 4)
    a1 = append(a1, 5)
    a1 = append(a1, 6)

    fmt.Println(a1)
    fmt.Println(a1[2:4])
    fmt.Println(a1[:4])
    fmt.Println(a1[2:])

}
