package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
)

// https://gobyexample.com/values

func main() {

	var tab = []float64{1.2, 2.2, 3.3}

	fmt.Println(tab)

	tab_bytes, err := json.Marshal(tab)
	if err != nil {
		panic(err)
	}

	fmt.Println(tab_bytes)

	err = ioutil.WriteFile("foo.dat", tab_bytes, 0644)
	if err != nil {
		panic(err)
	}
}
