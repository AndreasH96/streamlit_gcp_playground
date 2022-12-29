from PIL import Image, ImageDraw, ImageFont

def draw_annotations_on_image(image, annotations):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    for annotation in annotations["localized_object_annotations"]:
        bounding = annotation["bounding_poly"]["normalized_vertices"]
        min_X, max_X = min([b["x"] for b in bounding]) * \
            im.size[0], max([b["x"] for b in bounding])*im.size[0]
        min_Y, max_Y = min([b["y"] for b in bounding]) * \
            im.size[1], max([b["y"] for b in bounding])*im.size[1]

        rgb = im.getpixel((min_X, min_Y))
        complementaryC = complementaryColor(rgb)
        draw.rectangle([(min_X, min_Y), (max_X, max_Y)],
                       width=2, outline=complementaryC)
        text = annotation["name"]
        font = ImageFont.truetype('./fonts/Gidole-Regular.ttf', size=24)

        bbox = draw.textbbox((min_X+5, min_Y),text,font=font)
        draw.rectangle(bbox,fill=complementaryColor(complementaryC))
        draw.text((min_X+5, min_Y),
                  text, font=font, fill=complementaryC)

    return im


def complementaryColor(rgb):
    """Returns either black or white in RGB depending on the brightness of the input color
    """
    comp = [ (255 -a) for a in rgb]
   # Y =  0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    denom = 255*3
    v =  0 if rgb[0]/denom + rgb[1]/denom + rgb[2]/denom > 0.5 else 255
    comp = [v,v,v]
    


    return tuple(comp)

""" st.subheader(
        "Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24)
    )
    filtered = data[
        (data[DATE_TIME].dt.hour >= hour) & (
            data[DATE_TIME].dt.hour < (hour + 1))
    ]
    hist = np.histogram(filtered[DATE_TIME].dt.minute,
                        bins=60, range=(0, 60))[0]
    chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

    st.altair_chart(
        alt.Chart(chart_data)
        .mark_area(
            interpolate="step-after",
        )
        .encode(
            x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
            y=alt.Y("pickups:Q"),
            tooltip=["minute", "pickups"],
        ),
        use_container_width=True,
    )

    if st.checkbox("Show raw data", False):
        st.subheader(
            "Raw data by minute between %i:00 and %i:00" % (
                hour, (hour + 1) % 24)
        )
        st.write(data)
 """