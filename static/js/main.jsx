
const SideBarNav = (props) => {
  return (
    <ul>
      <li>Home</li>
      <li>Login</li>
    </ul>
  )
}

const PageOne = (props) => {
  return (
    <div>This is the first page.</div>
  )
}

const PageTwo = (props) => {
  return (
    <div>This is the second page.</div>
  )
}

const SideBarNav = (props) => {
  return (
    <ul>
      <li>Home</li>
      <li>Login</li>
    </ul>
  )
}

const MainSubContent = (props) => {
  return (
    <div></SubContent></div>

  )
}

const MainContent = (props) => {
  const [currentPage, setCurrentPage] = React.useState(0);
  function rendercontent() {
    if (currentPage === 0) {
      return <PageOne></PageOne>
    }
    if (currentPage === 1) {
      return <PageTwo></PageTwo>
    }
  }
  return (
    <button onClick={()=> setCurrentPage(1)}>Page One</button>
    <button onClick={()=> setCurrentPage(2)}>Page One</button>
    {renderContent()}
  )
}


const App = (props) => {
  return (
    <div>
      <SideBarNav></SideBarNav>
    </div>
  )
}

ReactDOM.render(<App/>, document.querySelector('#root'));