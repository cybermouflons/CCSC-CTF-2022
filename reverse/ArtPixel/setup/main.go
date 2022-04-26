package main

import (
	"flag"
	"fmt"
	"image"
	"image/color"
	"image/png"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type checks struct {
	c1 bool
	c2 bool
}
type differences struct {
	old_abs uint8
	old     int16
	new     int16
}
type pixels_groups struct {
	p1 uint8
	p2 uint8
}

type range_table struct {
	base  uint8
	width uint8
}

func stringToBin(s string) (binString string) {
	for _, c := range s {
		binString = fmt.Sprintf("%s%.8b", binString, c)
	}
	return
}

func convertToGrayscale(cover *image.Image, gray *image.Gray) {
	for y := min_y; y < max_y; y++ {
		for x := min_x; x < max_x; x++ {
			gray.Set(x, y, (*cover).At(x, y))
		}
	}
}

func calculateOldDifference(p1, p2 uint8) differences {
	var diffs differences
	diffs.old = int16(p2) - int16(p1)
	if p1 < p2 {
		diffs.old_abs = p2 - p1
	} else {
		diffs.old_abs = p1 - p2
	}
	return diffs
}

func calculateNewDifference(old_diff int16, base uint8, secret int64) int16 {
	var new_diff int16
	if old_diff > 0 {
		new_diff = int16(base + uint8(secret))
	} else {
		new_diff = -int16((base + uint8(secret)))
	}
	return new_diff

}

func findWidth(diff uint8) range_table {
	switch {
	case diff > 7 && diff < 16:
		return range_table{base: 8, width: 3}
	case diff > 15 && diff < 32:
		return range_table{base: 16, width: 4}
	default:
		return range_table{base: 0, width: 0}
	}
}

func calculateNewPixelValues(old_pixel1, old_pixel2 uint8, diffs *differences) pixels_groups {
	var average float64
	var new_pixels pixels_groups
	var check bool

	average = (float64(diffs.new) - float64(diffs.old)) / 2.0
	check = true

	if average < 0 {
		average = math.Abs(average)
		check = false
	}
	if diffs.old%2 == 0 {
		if check {
			new_pixels.p1 = old_pixel1 - uint8(math.Floor(average))
			new_pixels.p2 = old_pixel2 + uint8(math.Ceil(average))

		} else {
			new_pixels.p1 = old_pixel1 + uint8(math.Floor(average))
			new_pixels.p2 = old_pixel2 - uint8(math.Ceil(average))

		}
	} else {
		if check {
			new_pixels.p1 = old_pixel1 - uint8(math.Ceil(average))
			new_pixels.p2 = old_pixel2 + uint8(math.Floor(average))

		} else {
			new_pixels.p1 = old_pixel1 + uint8(math.Ceil(average))
			new_pixels.p2 = old_pixel2 - uint8(math.Floor(average))

		}

	}
	return new_pixels
}

func checkPossibility(secret **string, old_pixel1, old_pixel2 uint8, new_pixels *pixels_groups) checks {
	var c checks
	var err error
	var secret_decimal int64

	c.c1 = false

	//calculates the difference between the pixels
	diffs := calculateOldDifference(old_pixel1, old_pixel2)

	//calculates the range table
	table := findWidth(diffs.old_abs)

	if table.base != 0 {

		if len(**secret) >= int(table.width) {
			secret_decimal, err = strconv.ParseInt((**secret)[:table.width], 2, 64)

			if err != nil {
				panic(err)
			}
		} else {
			//pad the data
			pad := int(table.width) - len(**secret)
			secret_decimal, err = strconv.ParseInt((**secret)[:len(**secret)]+strings.Repeat("0", pad), 2, 64)
			if err != nil {
				panic(err)
			}
		}
		diffs.new = calculateNewDifference(diffs.old, table.base, secret_decimal)

		temp := calculateNewPixelValues(old_pixel1, old_pixel2, &diffs)

		(*new_pixels) = temp

		c.c1 = true

		if len(**secret) < int(table.width) {
			(**secret) = (**secret)[len(**secret):]

		} else {
			(**secret) = (**secret)[table.width:]
		}

	}

	if len(**secret) == 0 {
		fmt.Printf("[*] All the bits have been embedded \n")
		return checks{c.c1, true}
	} else {
		return checks{c.c1, false}
	}
}

func update_pixels(cover **image.Gray, new_pixels *pixels_groups, x, y, direction int) {
	(**cover).SetGray(x, y, color.Gray{new_pixels.p1})
	(**cover).SetGray(x+direction, y, color.Gray{new_pixels.p2})
}

func checkBrigthness(p1, p2 uint8) bool {
	if p1 > threshold && p2 > threshold {
		return true
	} else {
		return false
	}
}
func selectPixels(cover **image.Gray, direction, x, y int) pixels_groups {
	var pix pixels_groups
	pix.p1 = (**cover).GrayAt(x, y).Y
	pix.p2 = (**cover).GrayAt(x+direction, y).Y
	return pix
}

func iteratePixels(cover *image.Gray, secret *string) {
	var check checks
	var new_pixels pixels_groups
	var direction = 1

	fmt.Printf("[*] Iterating pixels...\n")

	for y := min_y; y < max_y; y++ {
		if direction == 1 {
			for x := min_x; x < max_x; x += 2 {
				old_pixels := selectPixels(&cover, direction, x, y)
				tau_check := checkBrigthness(old_pixels.p1, old_pixels.p2)
				if tau_check {
					check = checkPossibility(&secret, old_pixels.p1, old_pixels.p2, &new_pixels)

					if check.c1 {
						update_pixels(&cover, &new_pixels, x, y, direction)
					}
					if check.c2 {
						return
					}

				}
			}
			direction = -1
		} else {
			for x := max_x - 1; x > min_x; x -= 2 {

				old_pixels := selectPixels(&cover, direction, x, y)
				tau_check := checkBrigthness(old_pixels.p1, old_pixels.p2)
				if tau_check {
					check = checkPossibility(&secret, old_pixels.p1, old_pixels.p2, &new_pixels)

					if check.c1 {

						update_pixels(&cover, &new_pixels, x, y, direction)
					}
					if check.c2 {
						return
					}
				}
			}
			direction = 1
		}
	}
}

var min_x, max_x, min_y, max_y int
var threshold uint8

func main() {
	coverPtr := flag.String("cover", "", "Cover Image")
	secretPtr := flag.String("secret", "", "Secret Data")
	dirPtr := flag.String("dir", "stego.png", "Output Directory")

	flag.Parse()

	if len(os.Args) < 2 {
		flag.Usage()
		os.Exit(1)
	}

	cover, err := os.Open(*coverPtr)
	if err != nil {
		log.Fatal(err)
	}
	defer cover.Close()

	coverImg, err := png.Decode(cover)
	if err != nil {
		log.Fatal(err)
	}

	min_x = coverImg.Bounds().Min.X
	max_x = coverImg.Bounds().Max.X
	min_y = coverImg.Bounds().Min.Y
	max_y = coverImg.Bounds().Max.Y


	//converts secret to bits
	secret := stringToBin(*secretPtr)

	if len(secret) == 0 {
		os.Exit(1)
	}

	threshold = 15

	//creates grayscale images
	grayImg := image.NewGray(image.Rect(min_x, min_y, max_x, max_y))

	//converts image to grayscale
	convertToGrayscale(&coverImg, grayImg)

	f, err := os.Create(*dirPtr)

	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	//main function
	iteratePixels(grayImg, &secret)

	png.Encode(f, grayImg)
}
