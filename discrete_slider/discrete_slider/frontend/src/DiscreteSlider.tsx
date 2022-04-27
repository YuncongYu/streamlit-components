import { ComponentProps, Streamlit, StreamlitComponentBase, withStreamlitConnection } from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Slider } from "@material-ui/core"
import { styled } from "@material-ui/core/styles"

interface State {
  selectedIndex: number;
}

interface Mark {
  value: number;
  label: string;
}

function createMarks(labels: string[]): Mark[] {
  return labels.map((label, index) => ({ value: index, label: label }))
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class DiscreteSlider extends StreamlitComponentBase<State> {

  public constructor(props: ComponentProps) {
    super(props)

    let selectedIndex = 0
    this.state = { selectedIndex }
  }

  public render = (): ReactNode => {
    const vMargin = 7
    const hMargin = 20
    const options = this.props.args.options
    let selectedIndex = 0

    const StyledSlider = styled(Slider)({
      margin: `${vMargin}px ${hMargin}px`,
      width: this.props.width - (hMargin * 2),
    })

    return (
      <StyledSlider
        defaultValue={this.state.selectedIndex}
        min={0}
        max={options.length - 1}
        step={null}
        valueLabelDisplay="off"
        marks={createMarks(options)}
        onChangeCommitted={(event, value) => {
          const selectedIndex = Number(value)
          this.setState(
            { selectedIndex: selectedIndex },
            () => Streamlit.setComponentValue(selectedIndex)
          );
          // Streamlit.setComponentValue(selectedOption)
        }}
      />
    )
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(DiscreteSlider)
