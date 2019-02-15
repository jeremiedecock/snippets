package main

import "fmt"

func main() {

    m := make( map[string]int )

    m["one"] = 1
    m["two"] = 2

    fmt.Println(m)

    v1 := m["one"]
    fmt.Println("one: ", v1)

    fmt.Println("len:", len(m))

    delete(m, "two")
    fmt.Println("map:", m)

    _, prs := m["three"]
    if prs == true {
        fmt.Println("three is present")
    } else {
        fmt.Println("three is absent")
    }

    m2 := map[string]int{"one": 1, "two": 2}
    fmt.Println("map:", m2)

}
